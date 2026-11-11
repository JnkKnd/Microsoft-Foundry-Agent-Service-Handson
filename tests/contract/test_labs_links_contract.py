"""Documentation contracts for Portal bootstrap, GitHub assets and Dev Containers."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from itertools import pairwise
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
COPILOT_INSTRUCTIONS = REPO_ROOT / ".github" / "copilot-instructions.md"
LABS_DIR = REPO_ROOT / "labs"
ENVIRONMENTS = REPO_ROOT / "docs" / "participant" / "environments"
CODESPACES_GUIDE = ENVIRONMENTS / "codespaces.md"
LOCAL_GUIDE = ENVIRONMENTS / "local-dev-container.md"
LEGACY_GUIDE = ENVIRONMENTS / "cloud-shell.md"
HISTORY_START = (
    "<details>\n<summary>Historical procedure</summary>\n\n<!-- historical-content:start -->\n"
)
HISTORY_END = "<!-- historical-content:end -->\n</details>\n"
ADMIN_GUIDE = REPO_ROOT / "docs" / "admin" / "prerequisites.md"
PARTICIPANT_PREREQUISITES = REPO_ROOT / "docs" / "participant" / "prerequisites.md"
CORE_LABS = {
    int(name.partition("-")[0]): LABS_DIR / name
    for name in (
        "01-setup.md",
        "02-prompt-agent.md",
        "03-rag-foundry-iq.md",
        "04-tools-toolbox.md",
        "05-evaluation.md",
        "06-optimization.md",
        "07-agent-framework-harness.md",
        "08-hosted-multi-agent.md",
        "09-observability-cleanup.md",
    )
}
PATH_INSTRUCTIONS = sorted((REPO_ROOT / ".github" / "instructions").rglob("*.instructions.md"))
AI_GUIDANCE = [REPO_ROOT / "AGENTS.md", COPILOT_INSTRUCTIONS, *PATH_INSTRUCTIONS]
DEVELOPMENT_DIR = REPO_ROOT / "docs" / "development"
DEVELOPER_DOCUMENTS = [
    REPO_ROOT / ".devcontainer" / "README.md",
    REPO_ROOT / "infra" / "README.md",
    REPO_ROOT / "src" / "travel-api" / "README.md",
    REPO_ROOT / "assets" / "README.md",
]
DOCUMENTS = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "README.en.md",
    *sorted(LABS_DIR.rglob("*.md")),
    *sorted((REPO_ROOT / "docs").rglob("*.md")),
    *sorted((REPO_ROOT / "instructor").rglob("*.md")),
    REPO_ROOT / "src" / "hosted-agent" / "README.md",
]
REPOSITORY = "JnkKnd/Microsoft-Foundry-Agent-Service-Handson"
COMMON_ASSETS = (
    "assets/skills/travel-estimation.zip",
    "assets/skills/preapproval-simulation.zip",
    "assets/openapi/travel-ops.openapi.json",
)
RETIRED_REFERENCES = (
    "environments/azure-ml.md",
    "00-azureml-setup.ipynb",
    "setup_azureml.py",
    "Azure ML",
    "Azure Machine Learning",
    "Standard_DS3_v2",
    "Storage browser",
    "participantDownload",
    "foundry-workshop-files.zip",
    "portal-assets/",
    "Upload folder",
    "conda run",
    "environments/cloud-shell.md",
    "setup-cloud-shell.sh",
    "activate-cloud-shell.sh",
    "scripts/setup.sh",
    "scripts/destroy.sh",
    "terraform_outputs",
)
RETIRED_IMAGES = (
    "lab01-azureml-compute.png",
    "lab01-azureml-idle-shutdown.png",
    "lab01-azureml-upload.png",
    "lab01-bootstrap-outputs.png",
    "lab01-private-zip-download.png",
)
LINK_PATTERN = re.compile(r"\[[^\]\n]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
JAPANESE_TEXT = re.compile(r"[\u3041-\u3096\u30a1-\u30fa\u3400-\u4dbf\u4e00-\u9fff]")


def normalized(text: str) -> str:
    return " ".join(text.replace("**", "").replace("`", "").split())


def assert_no_unexpected_japanese(text: str) -> None:
    assert not JAPANESE_TEXT.search(text), "unexpected Japanese documentation text"


def assert_public_source_revision(revision: str) -> None:
    assert revision == "English" or re.fullmatch(r"[a-f0-9]{40}", revision), (
        f"expected English browsing branch or immutable commit, got {revision!r}"
    )


def assert_in_order(text: str, steps: tuple[str, ...]) -> None:
    text = normalized(text)
    position = 0
    for step in steps:
        index = text.find(step, position)
        assert index >= 0, f"missing or out-of-order step: {step}"
        position = index + len(step)


def current_document_text(path: Path, text: str) -> str:
    if (
        path == LEGACY_GUIDE
        and text.count(HISTORY_START) == 1
        and text.count(HISTORY_END) == 1
        and text.endswith(HISTORY_END)
    ):
        return text.partition(HISTORY_START)[0]
    return text


def read(path: Path) -> str:
    return current_document_text(path, path.read_text(encoding="utf-8"))


def links(path: Path) -> list[str]:
    return LINK_PATTERN.findall(read(path))


def local_links() -> list[tuple[Path, str]]:
    return [
        (path, target)
        for path in [*DOCUMENTS, *AI_GUIDANCE, *DEVELOPER_DOCUMENTS]
        for target in links(path)
        if not urlsplit(target).scheme
    ]


def markdown_anchors(text: str) -> set[str]:
    anchors = set(re.findall(r'<a\s+(?:id|name)="([^"]+)"', text))
    counts: dict[str, int] = {}
    for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.MULTILINE):
        slug = re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        anchors.add(f"{slug}-{count}" if count else slug)
        counts[slug] = count + 1
    return anchors


def assert_local_link_resolves(source: Path, target: str) -> None:
    parsed = urlsplit(target)
    resolved = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
    assert resolved.is_file(), f"{source} -> {target}"
    if parsed.fragment and resolved.suffix == ".md":
        assert unquote(parsed.fragment) in markdown_anchors(read(resolved)), (
            f"{source} -> missing anchor {target}"
        )


def instruction_patterns(text: str) -> list[str]:
    match = re.fullmatch(r"---\n(.*?)\n---\n(.+)", text, re.DOTALL)
    assert match and match.group(2).strip(), "expected frontmatter and instruction body"
    metadata = yaml.safe_load(match.group(1))
    assert isinstance(metadata, dict), "frontmatter must be a mapping"
    for key in ("description", "applyTo"):
        assert isinstance(metadata.get(key), str) and metadata[key].strip(), (
            f"expected nonempty {key}"
        )
    patterns = [pattern.strip() for pattern in metadata["applyTo"].split(",")]
    assert all(patterns), "applyTo must not contain empty patterns"
    return patterns


@pytest.mark.parametrize(
    ("source", "target"),
    local_links(),
    ids=[f"{path.relative_to(REPO_ROOT)}::{target}" for path, target in local_links()],
)
def test_local_document_link_resolves(source: Path, target: str) -> None:
    assert_local_link_resolves(source, target)


@pytest.mark.parametrize("target", ["missing.md", "guide.md#missing", "#missing"])
def test_local_link_contract_rejects_broken_targets(tmp_path: Path, target: str) -> None:
    source = tmp_path / "instructions.md"
    source.write_text("# Instructions\n", encoding="utf-8")
    (tmp_path / "guide.md").write_text("# Guide\n", encoding="utf-8")
    with pytest.raises(AssertionError, match=re.escape(target)):
        assert_local_link_resolves(source, target)


@pytest.mark.parametrize("target", ["guide.md#guide", "#instructions"])
def test_local_link_contract_accepts_existing_headings(tmp_path: Path, target: str) -> None:
    source = tmp_path / "instructions.md"
    source.write_text("# Instructions\n", encoding="utf-8")
    (tmp_path / "guide.md").write_text("# Guide\n", encoding="utf-8")
    assert_local_link_resolves(source, target)


@pytest.mark.parametrize(
    "text",
    [
        "# No frontmatter\n",
        '---\ndescription: Guide\napplyTo: "**/*.md"\n# No closing delimiter\n',
        '---\napplyTo: "**/*.md"\n---\n# Missing description\n',
        "---\ndescription: Guide\n---\n# Missing applyTo\n",
        '---\ndescription: Guide\napplyTo: ""\n---\n# Empty applyTo\n',
        '---\ndescription: Guide\napplyTo: ["*.md"]\n---\n# Not a string\n',
        '---\ndescription: Guide\napplyTo: "*.md,"\n---\n# Empty pattern\n',
        '---\ndescription: Guide\napplyTo: "**/*.md"\n---\n',
        "---\n- not-a-mapping\n---\n# Invalid metadata\n",
        "---\ndescription: [\n---\n# Malformed YAML\n",
    ],
)
def test_instruction_contract_rejects_invalid_frontmatter(text: str) -> None:
    with pytest.raises((AssertionError, yaml.YAMLError)):
        instruction_patterns(text)


def test_instruction_contract_accepts_multiple_patterns() -> None:
    text = '---\ndescription: Guide\napplyTo: "**/*.md, docs/images/**"\n---\n# Guide\n'
    assert instruction_patterns(text) == ["**/*.md", "docs/images/**"]


def test_path_instructions_are_discovered_and_linked_from_developer_guide() -> None:
    assert PATH_INSTRUCTIONS, "expected repository-specific path instructions"
    guide = DEVELOPMENT_DIR / "README.md"
    targets = {
        (guide.parent / urlsplit(target).path).resolve()
        for target in links(guide)
        if not urlsplit(target).scheme
    }
    checked_sources = {source for source, _ in local_links()}
    for path in PATH_INSTRUCTIONS:
        instruction_patterns(read(path))
        assert path.resolve() in targets, f"developer guide does not link to {path.name}"
        assert path in checked_sources, f"no documentation links checked for {path.name}"


@pytest.mark.parametrize("readme", [REPO_ROOT / "README.md", REPO_ROOT / "README.en.md"])
def test_readmes_link_all_labs_and_supported_environments(readme: Path) -> None:
    text = read(readme)
    if readme.name == "README.en.md" and "compatibility entry" in text:
        assert "README.md" in links(readme)
        readme = REPO_ROOT / "README.md"
    targets = links(readme)
    for index, lab in CORE_LABS.items():
        assert lab.is_file()
        assert f"[Lab {index}](labs/{lab.name})" in read(readme)
    for guide in ("custom-template.md", "codespaces.md", "local-dev-container.md"):
        assert f"docs/participant/environments/{guide}" in targets


def test_core_labs_link_to_next_lab() -> None:
    for current, following in pairwise(CORE_LABS.values()):
        assert following.name in links(current)


@pytest.mark.parametrize("path", DOCUMENTS, ids=lambda path: str(path.relative_to(REPO_ROOT)))
def test_documents_do_not_reintroduce_retired_handoffs(path: Path) -> None:
    text = read(path)
    for retired in RETIRED_REFERENCES:
        assert retired not in text, f"{path.relative_to(REPO_ROOT)} retains {retired}"


def test_history_filter_is_limited_to_the_explicit_legacy_section() -> None:
    current = "# Current procedure references\n"
    archived = f"{current}{HISTORY_START}scripts/setup.sh\n{HISTORY_END}"
    assert current_document_text(LEGACY_GUIDE, archived) == current
    assert current_document_text(CODESPACES_GUIDE, archived) == archived
    for malformed in (
        archived.replace(HISTORY_START, ""),
        archived.replace(HISTORY_END, ""),
        archived + "scripts/setup.sh\n",
        archived.replace(HISTORY_START, HISTORY_START * 2),
    ):
        assert current_document_text(LEGACY_GUIDE, malformed) == malformed


def test_legacy_guide_preserves_history_and_routes_to_supported_guides() -> None:
    source = LEGACY_GUIDE.read_text(encoding="utf-8")
    assert source.count(HISTORY_START) == source.count(HISTORY_END) == 1
    assert source.endswith(HISTORY_END)
    current = read(LEGACY_GUIDE)
    for token in (
        "historical documentation",
        "not used by the current configuration",
        "links",
        "do not guarantee current availability",
    ):
        assert token in normalized(current)
    for target in ("custom-template.md", "codespaces.md", "local-dev-container.md"):
        assert target in links(LEGACY_GUIDE)


def test_formatter_preserves_history_but_formats_current_sources(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_bytes((REPO_ROOT / "pyproject.toml").read_bytes())
    archived = tmp_path / LEGACY_GUIDE.relative_to(REPO_ROOT)
    archived.parent.mkdir(parents=True)
    original = LEGACY_GUIDE.read_bytes()
    archived.write_bytes(original)
    current_guide = tmp_path / CODESPACES_GUIDE.relative_to(REPO_ROOT)
    current_guide.write_text("```python\nvalue=1\n```\n", encoding="utf-8")
    current_code = tmp_path / "current.py"
    current_code.write_text("value=1\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "ruff", "format", "--no-cache", "."],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert archived.read_bytes() == original
    assert current_guide.read_text(encoding="utf-8") == "```python\nvalue = 1\n```\n"
    assert current_code.read_text(encoding="utf-8") == "value = 1\n"


def test_runbook_covers_every_lab_and_distinguishes_incomplete_runs() -> None:
    runbook = REPO_ROOT / "instructor" / "runbook.md"
    text = read(runbook)
    for lab in CORE_LABS.values():
        assert f"../labs/{lab.name}" in links(runbook)
    for token in (
        "every participant Lab (1\u20139)",
        "same revision",
        "Partial",
        "Incomplete",
        "Not performed",
        "Interrupted",
        "Run all 7 evaluation rows",
        "Run optimization with 1 candidate",
        "plan",
        "execute",
        "todos",
        "cleanup",
    ):
        assert token in normalized(text)
    assert "verify representative operations" not in text
    instructions = read(COPILOT_INSTRUCTIONS)
    assert "../instructor/runbook.md" in links(COPILOT_INSTRUCTIONS)
    for token in (
        "all Labs (1-9)",
        "same revision",
        "incomplete",
        "not run",
        "interrupted",
        "prior approval",
    ):
        assert token in normalized(instructions)
    assert "representative labs" not in instructions


def test_repository_documentation_language_policy_preserves_english_primary_entry() -> None:
    instructions = read(COPILOT_INSTRUCTIONS)
    for token in ("docs/", "English", "README.md", "README.en.md", "UI", "identifiers"):
        assert token in instructions
    assert "English is the source language" in normalized(instructions)
    assert "README.md is the primary entry point" in normalized(instructions)


def test_agents_routes_to_github_without_duplicating_the_moved_policies() -> None:
    agents = read(REPO_ROOT / "AGENTS.md")
    assert ".github/copilot-instructions.md" in links(REPO_ROOT / "AGENTS.md")
    for token in (
        "## Documentation language and source of truth",
        "## Portal E2E",
        "all Labs (1-9)",
        "README.en.md",
    ):
        assert token not in agents


def test_documentation_layout_separates_audiences() -> None:
    for name in ("README.md", "architecture.md", "feature-support-matrix.md"):
        assert (DEVELOPMENT_DIR / name).is_file()
        assert not (REPO_ROOT / ".github" / "development" / name).exists()
    for name in ("architecture.md", "feature-support-matrix.md"):
        assert not (REPO_ROOT / "docs" / name).exists()
    assert (REPO_ROOT / "docs" / "participant" / "costs-and-cleanup.md").is_file()
    assert not (REPO_ROOT / "docs" / "costs-and-cleanup.md").exists()
    for target in ("docs/README.md", "docs/development/README.md", "instructor/README.md"):
        assert target in links(REPO_ROOT / "README.md")
        english_links = links(REPO_ROOT / "README.en.md")
        assert target in english_links or (
            "README.md" in english_links
            and "compatibility entry" in read(REPO_ROOT / "README.en.md")
        )
    for target in ("architecture.md", "feature-support-matrix.md", "../../infra/README.md"):
        assert target in links(DEVELOPMENT_DIR / "README.md")
    assert "development/README.md" in links(REPO_ROOT / "docs" / "README.md")
    for target in ("../docs/development/README.md", "../docs/development/architecture.md"):
        assert target in links(COPILOT_INSTRUCTIONS)


@pytest.mark.parametrize(
    "relative_path",
    [
        "AGENTS.md",
        ".devcontainer/README.md",
        "docs/development/README.md",
        "docs/development/architecture.md",
        "docs/development/feature-support-matrix.md",
        "docs/README.md",
        "docs/images/ATTRIBUTION.md",
        "infra/README.md",
        "instructor/README.md",
        "labs/optional/README.md",
    ],
)
def test_basic_documentation_has_english_titles(relative_path: str) -> None:
    title = read(REPO_ROOT / relative_path).splitlines()[0]
    assert title.startswith("# ")
    assert re.search(r"[A-Za-z]", title)
    assert_no_unexpected_japanese(title)


@pytest.mark.parametrize(
    "path",
    list(dict.fromkeys([*DOCUMENTS, *AI_GUIDANCE, *DEVELOPER_DOCUMENTS])),
    ids=lambda path: str(path.relative_to(REPO_ROOT)),
)
def test_documentation_has_no_unexpected_japanese(path: Path) -> None:
    assert_no_unexpected_japanese(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("text", ["\u65e5\u672c\u8a9e", "\u304b\u306a", "\u30ab\u30ca"])
def test_english_language_contract_rejects_japanese(text: str) -> None:
    with pytest.raises(AssertionError, match="unexpected Japanese"):
        assert_no_unexpected_japanese(text)


@pytest.mark.parametrize("text", ["English · UI → ✓ \u00d7 ±", "JPY 1,500 — 2026-09-10", "API_ID"])
def test_english_language_contract_accepts_unicode_and_identifiers(text: str) -> None:
    assert_no_unexpected_japanese(text)


def test_maintainer_guides_expose_translated_contract_anchors() -> None:
    assert {
        "getting-started-with-development",
        "ai-configuration-responsibilities",
        "working-with-ai-on-changes",
        "change-targets-and-checks",
    } <= markdown_anchors(read(DEVELOPMENT_DIR / "README.md"))
    assert "model-quotas" in markdown_anchors(read(ADMIN_GUIDE))
    assert "real-environment-validation-scope" in markdown_anchors(
        read(REPO_ROOT / "instructor" / "runbook.md")
    )


def test_developer_quickstart_covers_setup_validation_and_change_ownership() -> None:
    guide = read(DEVELOPMENT_DIR / "README.md")
    for token in (
        "Dev Containers: Reopen in Container",
        "postCreateCommand",
        "WORKSHOP_MANAGEMENT_PYTHON",
        "WORKSHOP_HOSTED_PYTHON",
        "make lint",
        "make test-hosted",
        "make assets-check",
        "make bicep-validate",
        "make validate",
        "Change targets",
        "source of truth",
        "real-environment",
    ):
        assert token in guide
    workflow = read(REPO_ROOT / ".github" / "workflows" / "validate.yml")
    pinned_install = re.search(r"az bicep install --version v[\d.]+", workflow)
    assert pinned_install and pinned_install.group() in guide
    targets = {
        target
        for match in re.finditer(r"^([\w -]+):", read(REPO_ROOT / "Makefile"), re.MULTILINE)
        for target in match.group(1).split()
    }
    for match in re.finditer(r"^make ([\w -]+)$", guide, re.MULTILINE):
        assert set(match.group(1).split()) <= targets


@pytest.mark.parametrize("name", ["README.md", "README.en.md"])
def test_agenda_distinguishes_planning_estimates_from_setup_time(name: str) -> None:
    path = REPO_ROOT / name
    text = read(path)
    if name == "README.en.md" and "compatibility entry" in text:
        assert "README.md" in links(path)
        path = REPO_ROOT / "README.md"
        text = read(path)
    durations = [
        int(value)
        for value in re.findall(r"^\|[^|]+\|[^|]+\|\s*(\d+)\s*(?:分|min)\s*\|", text, re.M)
    ]
    assert len(durations) == 9
    total_pattern = r"total \*\*(\d+) minutes"
    declared_total = re.search(total_pattern, text)
    assert declared_total and int(declared_total.group(1)) == sum(durations)
    assert "instructor/README.md" in links(path)
    for token in ("Lab 1", "not measured", "event announcement", "in advance", "on the day"):
        assert token in text


def test_readmes_distinguish_local_harness_from_separate_hosted_workflow() -> None:
    for name in ("README.md", "README.en.md"):
        text = read(REPO_ROOT / name)
        if name == "README.en.md" and "compatibility entry" in text:
            assert "README.md" in links(REPO_ROOT / name)
            text = read(REPO_ROOT / "README.md")
        text = normalized(text)
        assert (
            "In Lab 7, run and compare Plain Agent and Harness Agent inside the Dev Container"
            in text
        )
        assert "In Lab 8, build a separate sequential workflow" in text


@pytest.mark.parametrize(
    "path",
    [
        REPO_ROOT / "AGENTS.md",
        DEVELOPMENT_DIR / "architecture.md",
        DEVELOPMENT_DIR / "feature-support-matrix.md",
    ],
)
def test_overviews_reference_capacity_source_without_duplicating_numbers(path: Path) -> None:
    assert not re.search(r"\d+K TPM", read(path))
    assert any(
        target.endswith("docs/admin/prerequisites.md#model-quotas") for target in links(path)
    )


def test_lab_one_creates_rg_then_deploys_defaults_and_waits_for_initialization() -> None:
    lab = read(CORE_LABS[1])
    assert_in_order(
        lab,
        (
            "Resource groups > Create",
            "Review + create > Create",
            "Deploy a custom template",
            "Load file",
            "Subscription",
            "Resource group",
            "defaults",
            "Review + create > Create",
            "Deployment Scripts",
            "Succeeded",
            "workshopContext",
            "setup_status = complete",
            "foundryPortalUrl",
        ),
    )
    for token in (
        "Manually create one dedicated RG",
        "Create new",
        "Participant Object Id Override",
        "empty",
    ):
        assert token in lab
    for output in ("resourceOutputs", "travelApiBaseUrl", "foundryPortalUrl"):
        assert output in lab


def test_public_source_links_use_english_or_published_revision() -> None:
    prefixes = (
        f"https://github.com/{REPOSITORY}/blob/",
        f"https://github.com/{REPOSITORY}/tree/",
        f"https://raw.githubusercontent.com/{REPOSITORY}/",
    )
    for document in DOCUMENTS:
        for target in links(document):
            for prefix in prefixes:
                if target.startswith(prefix):
                    revision, _, path = (
                        urlsplit(target).path.removeprefix(urlsplit(prefix).path).partition("/")
                    )
                    assert_public_source_revision(revision)
                    resolved = REPO_ROOT / unquote(path)
                    assert resolved.exists(), target
                    if (
                        revision == "English"
                        and resolved.suffix == ".md"
                        and urlsplit(target).fragment
                    ):
                        assert unquote(urlsplit(target).fragment) in markdown_anchors(
                            read(resolved)
                        ), f"{document.relative_to(REPO_ROOT)} -> missing anchor {target}"
    for document in (CORE_LABS[1], PARTICIPANT_PREREQUISITES):
        assert any(target.endswith("/infra/azuredeploy.json") for target in links(document))
    assert "../../assets/README.md" in links(PARTICIPANT_PREREQUISITES)


@pytest.mark.parametrize("revision", ["main", "latest", "a" * 39, "A" * 40, "not-a-sha"])
def test_public_source_revision_contract_rejects_mutable_or_invalid_pins(revision: str) -> None:
    with pytest.raises(AssertionError, match="English browsing branch or immutable commit"):
        assert_public_source_revision(revision)


@pytest.mark.parametrize("revision", ["English", "0123456789abcdef" * 2 + "01234567"])
def test_public_source_revision_contract_accepts_browsing_or_immutable_commit(
    revision: str,
) -> None:
    assert_public_source_revision(revision)


def test_release_assets_require_fixed_source_separately_from_branch_browsing() -> None:
    lab = normalized(read(CORE_LABS[4]))
    admin = normalized(read(ADMIN_GUIDE))
    assert "mutable browsing/download references, not release pins" in lab
    assert "pinned to a fixed source SHA" in lab
    assert "same public SHA for sourceRevision and distributed material references" in admin
    parameters = json.loads(read(REPO_ROOT / "infra" / "azuredeploy.json"))["parameters"]
    source = parameters["sourceRevision"]["defaultValue"]
    image = parameters["travelApiImageRef"]["defaultValue"]
    if source or image:
        assert re.fullmatch(r"[a-f0-9]{40}", source)
        assert re.fullmatch(r"ghcr\.io/jnkknd/[^@\s]+@sha256:[a-f0-9]{64}", image)
    else:
        for document in (REPO_ROOT / "README.md", PARTICIPANT_PREREQUISITES, CORE_LABS[1]):
            text = normalized(read(document))
            assert "not yet deployment-ready" in text or "unreleased English branch" in text
            assert "published" in text and "digest" in text
        assert "guards explicitly reject the empty source / image defaults" in admin


def test_portal_labs_read_arm_outputs_without_requiring_local_context() -> None:
    for index in (2, 3, 5, 6):
        text = read(CORE_LABS[index])
        assert "resourceOutputs" in text
        assert ".workshop/context.json" not in text
    for index in (3, 5, 6):
        assert "gpt-5.5" in read(CORE_LABS[index])
    assert "Microsoft Entra ID-authenticated Azure AI Search connection" in read(CORE_LABS[2])
    assert "contoso-travel-eval-live-subset" in read(CORE_LABS[5])
    assert "contoso-travel-optimizer-live-subset" in read(CORE_LABS[6])


def test_lab_four_downloads_shared_zip_files_and_replaces_only_the_openapi_server() -> None:
    lab = read(CORE_LABS[4])
    targets = links(CORE_LABS[4])
    for asset in COMMON_ASSETS:
        assert any(
            target.startswith(f"https://raw.githubusercontent.com/{REPOSITORY}/")
            and target.endswith(f"/{asset}")
            for target in targets
        )
        assert (REPO_ROOT / asset).is_file()
    for token in (
        "Save these shared files to your PC",
        "SKILL.md",
        "at its root",
        "servers[0].url",
        "travelApiBaseUrl",
        "OpenAPI 3.0+ schema",
        "Project Managed Identity",
        "Publish",
    ):
        assert token in lab
    for skill in ("travel-estimation", "preapproval-simulation"):
        assert f"../data/skills/{skill}/SKILL.md" in targets


def test_codespaces_guides_browser_creation_login_and_two_input_setup() -> None:
    guide = read(CODESPACES_GUIDE)
    assert_in_order(
        guide,
        (
            "Code > Codespaces",
            "postCreateCommand",
            "Terminal > New Terminal",
            "az login --use-device-code",
            "00-setup.ipynb",
            "Python (Foundry Workshop)",
            "subscription ID",
            "RG name",
            ".workshop/context.json",
        ),
    )
    for token in (
        "GitHub and Azure Portal",
        "separate from Azure CLI sign-in",
        "scripts/configure_workshop.py",
        "workshopContext",
        "2.0",
        "resource_outputs.<key>.value",
        "~/.venvs/",
        "foundry-workshop",
        "foundry-hosted-agent",
        "3.12",
        "3.13",
    ):
        assert token in guide
    for target in links(CODESPACES_GUIDE):
        assert not target.startswith(
            ("https://codespaces.new/", "https://github.com/codespaces/new")
        )


def test_local_guide_uses_same_container_not_a_native_python_setup() -> None:
    guide = read(LOCAL_GUIDE)
    assert "Prerequisites for local execution" in guide
    for prerequisite in ("Git", "Visual Studio Code", "Dev Containers", "Docker", "Azure"):
        assert prerequisite in guide
    assert_in_order(
        guide,
        ("git clone", "Dev Containers: Reopen in Container", "codespaces.md#shared-steps"),
    )
    for unsupported in ("pip install", "python -m venv", "conda create", "conda activate"):
        assert unsupported not in guide


def test_documented_environment_interfaces_exist() -> None:
    for path in (
        ".devcontainer/devcontainer.json",
        "scripts/setup_dev_environment.py",
        "scripts/configure_workshop.py",
        "notebooks/00-setup.ipynb",
    ):
        assert (REPO_ROOT / path).is_file(), f"pending environment interface: {path}"
    assert not (ENVIRONMENTS / "azure-ml.md").exists()


def test_hosted_labs_use_hosted_kernel_and_confirm_management_actions() -> None:
    for index in (7, 8):
        text = read(CORE_LABS[index])
        for token in (
            "Codespaces",
            "local-dev-container.md",
            "00-setup.ipynb",
            "Python (Foundry Hosted Agent)",
            "foundry-hosted-agent",
            "resource_outputs.<key>.value",
        ):
            assert token in text
    lab_eight = read(CORE_LABS[8])
    for token in ("DEPLOY", "Agent name", "foundry-workshop", "venv", "3.12", "source ZIP"):
        assert token in lab_eight


def test_model_defaults_match_generated_template() -> None:
    parameters = json.loads(read(REPO_ROOT / "infra" / "azuredeploy.json"))["parameters"]
    admin = read(ADMIN_GUIDE)
    for model in ("primary", "evaluation", "embedding"):
        name = f"{model}ModelVersion"
        row = next(line for line in admin.splitlines() if f"`{name}`" in line)
        assert f"`{parameters[name]['defaultValue']}`" in row
    for model, capacity in (("gpt-5.6-luna", 40), ("gpt-5.5", 100), ("text-embedding-3-small", 40)):
        row = next(line for line in admin.splitlines() if f"`{model}`" in line)
        assert f"{capacity}K TPM" in row
    for token in (
        "sourceRevision",
        "published",
        "compatible",
        "participantObjectIdOverride",
        "bootstrapRunId",
        "enableBootstrapPolicyExclusion",
    ):
        assert token in admin


def test_cleanup_saves_results_before_hosted_codespace_and_rg_deletion() -> None:
    cleanup = read(CORE_LABS[9])
    assert_in_order(
        cleanup,
        (
            "Save All",
            "export",
            "Python (Foundry Hosted Agent)",
            "Agent name",
            "foundry-workshop",
            "all versions",
            "Stop codespace",
            "Delete",
            "Delete resource group",
            "verify the RG is gone",
        ),
    )
    assert "https://github.com/codespaces" in cleanup
    assert "only your dedicated RG" in cleanup
    assert "Deleting deployment history does not delete resources" in cleanup


@pytest.mark.parametrize("name", ["workshop-architecture", "workshop-learning-flow"])
def test_diagrams_preserve_text_geometry_and_current_flow(name: str) -> None:
    diagram = json.loads(read(REPO_ROOT / "docs" / "diagrams" / f"{name}.excalidraw"))
    svg = ET.parse(REPO_ROOT / "docs" / "images" / f"{name}.svg").getroot()
    assert diagram["type"] == "excalidraw" and diagram["version"] == 2
    assert svg.attrib["role"] == "img"
    elements = {element["id"]: element for element in diagram["elements"]}
    assert len(elements) == len(diagram["elements"])
    source_text = {
        key: normalized(element["text"])
        for key, element in elements.items()
        if element["type"] == "text"
    }
    svg_text = {
        node.attrib["id"]: normalized(" ".join(node.itertext()))
        for node in svg.iter("{http://www.w3.org/2000/svg}text")
    }
    assert svg_text == source_text
    labels = " ".join(source_text.values())
    for token in (
        "Resource groups > Create",
        "existing RG",
        "Deployment Scripts",
        "GitHub",
        "Codespaces",
        "local Dev Container",
        "Azure CLI",
        "00-setup.ipynb",
        "Python (Foundry Hosted Agent)",
        "Delete resource group",
        "verify deletion",
    ):
        assert token in labels
    for retired in RETIRED_REFERENCES:
        assert retired not in labels
    svg_rectangles = {
        node.attrib.get("id"): node for node in svg.iter("{http://www.w3.org/2000/svg}rect")
    }
    rectangles = [element for element in elements.values() if element["type"] == "rectangle"]
    for element in rectangles:
        for dimension in ("x", "y", "width", "height"):
            assert float(svg_rectangles[element["id"]].attrib[dimension]) == element[dimension]
        for child in rectangles:
            if (
                element["id"] != child["id"]
                and element["x"] <= child["x"]
                and element["y"] <= child["y"]
                and child["x"] + child["width"] <= element["x"] + element["width"]
                and child["y"] + child["height"] <= element["y"] + element["height"]
            ):
                assert element["backgroundColor"] == "transparent"
    for element in elements.values():
        if element["type"] != "text":
            continue
        assert element["width"] > 0
        assert element["height"] >= element["fontSize"] * 2.5 * len(element["text"].splitlines())
        assert element["strokeColor"] == "#000000"
        if container_id := element.get("containerId"):
            container = elements[container_id]
            assert {"id": element["id"], "type": "text"} in container["boundElements"]
            assert element["x"] >= container["x"] and element["y"] >= container["y"]
            assert element["x"] + element["width"] <= container["x"] + container["width"]
            assert element["y"] + element["height"] <= container["y"] + container["height"]


def test_retired_screenshots_are_removed_but_generic_completion_example_remains() -> None:
    images = REPO_ROOT / "docs" / "images"
    for filename in RETIRED_IMAGES:
        assert not (images / filename).exists()
    assert (images / "lab01-template-succeeded.png").is_file()
