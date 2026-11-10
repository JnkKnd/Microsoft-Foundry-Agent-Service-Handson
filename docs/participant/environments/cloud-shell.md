# Legacy Cloud Shell guide references

The old procedure on this page is **not used by the current configuration**.
It is historical documentation for the former Cloud Shell / JupyterLab environment.
For provisioning, follow the [environment setup guide](custom-template.md) to
[Lab 1](../../../labs/01-setup.md). Run Labs 7–8 in
[Codespaces](codespaces.md) or the [local Dev Container](local-dev-container.md).

The old body is retained to explain earlier decisions. Its commands, UI descriptions,
and links assume the configuration at that time and do not guarantee current availability.
Use the guides above for current operations and permission decisions.

<details>
<summary>Historical procedure</summary>

<!-- historical-content:start -->
# Execution environment guide — Azure Cloud Shell Bash + JupyterLab

Use Azure Portal **Cloud Shell** and JupyterLab through **Web preview**.
Run the **same Lab 7 / 8 notebooks** as Codespaces in a browser without installing
development tools on your PC. This is not a CLI replacement for notebook exercises.

After preparing this environment, return to Lab 1 step 2.
The former preflight step no longer exists; [current Lab 1](../../../labs/01-setup.md)
uses a different provisioning procedure. In the historical configuration,
Labs 2–9 shared Terraform, Portal operations, materials, and Azure resources.
[Back to environment prerequisites](../prerequisites.md)

> [!IMPORTANT]
> **Bash with persistent storage is mandatory.** Do not run Terraform in an ephemeral
> **No storage account required** session.
> Cloud Shell may terminate after 20 minutes of inactivity, losing running processes and kernel memory.
> Organizers must check the default limit of **20 concurrent users per tenant** in advance.

> [!WARNING]
> Cloud Shell compute is free, but Storage accounts / Azure Files and workshop Azure usage are billable.
> `exit` or closing the browser does not delete storage or Azure resources.
> Follow the [shutdown order](#stop) to avoid losing state.

### What automatic creation simplifies

Choosing **We will create a storage account for you** on first use avoids separately
creating the storage RG, Storage account, and Azure Files share.
The following JupyterLab setup is still required:

| Setup | Why it is needed |
|---|---|
| Verify persistent HOME | Retain Terraform state, materials, and two Python environments after disconnection |
| Standalone CPython 3.13 | Use the workshop version separately from Cloud Shell system Python |
| Root / Hosted `.venv` environments | Avoid mixing `azure-ai-projects==2.5.0` and Hosted Agent `<2.4` |
| JupyterLab / Jupyter Server / two kernelspecs | Run the same Lab 7 / 8 notebooks in separate dependency environments |
| Native Graphviz | Render the actual workflow SVG in Lab 8 |
| Web preview / authentication / relay compatibility | Safely connect the actual preview URL, port, password, Host / Origin / XSRF, and kernel channels |
| Two Terminals and reconnection steps | Run normal commands while Jupyter stays active and safely resume after a 20-minute disconnect |

Automatic Storage creation is useful simplification, but does not eliminate
Jupyter-specific setup, communication, or operations.

## 1. Check input values and organizational permission

Check these with the instructor/administrator and record only nonsecret values.
Use the record to reconnect storage and verify deletion targets at the end.

| Value | What to check |
|---|---|
| Subscription ID | Subscription assigned to the workshop |
| Workload resource group | Your dedicated RG created at the start of participant prerequisites, with your own **Owner** permissions |
| Cloud Shell Storage creation permissions | Personal testing, or subscription-level permission allowing Cloud Shell to create a dedicated RG / Storage account, such as Contributor or an equivalent custom role |
| Automatically generated Storage | Record the dedicated RG, Storage account, File share, and location after creation; do not confuse them with the Workload RG or Terraform-managed resources |
| Workshop URL / branch | Public GitHub repository HTTPS clone URL and branch designated by the instructor |
| Creation/deletion ownership | Whether Cloud Shell created a new dedicated RG for this workshop or an administrator assigned existing Storage; exactly what may be deleted |
| Existing Cloud Shell settings | If already used, securely record original `preferredLocation`, subscription / RG / account / share, and personal settings. Existing storage is not a deletion target |

Administrators check `Microsoft.CloudShell` / `Microsoft.Storage` registration,
Storage permissions/policies, browser HTTPS / WSS, and access to GitHub, GHCR, and package sources.
See [administrator prerequisites](../../admin/prerequisites.md);
the historical Cloud Shell-specific subsection is no longer part of the current guide.
A public clone needs no GitHub account, but does need network access to GitHub.
Prohibiting Codespaces and prohibiting GitHub/package downloads are separate policies.

If shared-key access or public networking is prohibited and standard Cloud Shell storage
cannot mount, stop and consult the administrator. Do not weaken policies, firewalls, or authentication.
Participants do not register providers, assign subscription-scope roles, change quotas,
or run `admin-preflight.sh --apply`, apart from first-use Cloud Shell Storage creation.

<a id="create-storage"></a>

## 2. Let Cloud Shell create your dedicated storage

Assuming personal testing or the creation permissions above, use the official automatic route.

1. Sign in to [Azure Portal](https://portal.azure.com/) with the target Azure account.
2. Open **Cloud Shell** at the top and select **Bash** on first use.
3. Under **Getting started**, select **Mount storage account**.
4. Select the recorded **Storage account subscription**, then **Apply**.
5. In **Mount storage account**, select **We will create a storage account for you**,
   then **Next**. Cloud Shell creates a dedicated new RG, Storage account, and Azure Files share.
6. When the Bash prompt appears, use **Manage files > Open file share**
   to inspect and record RG / account / share / location for final deletion.

Official steps:
[Get started with Azure Cloud Shell using persistent storage](https://learn.microsoft.com/azure/cloud-shell/get-started/new-storage)

> [!IMPORTANT]
> The destination is a new Cloud Shell-specific RG, not the existing workshop workload RG.
> It is not managed by `setup.sh` / `destroy.sh`. Each participant records only their
> own dedicated RG and deletes it after successful workload cleanup.

<details>
<summary>Only where new RGs are prohibited: manually create Storage in an existing RG</summary>

If an administrator already prepared a **dedicated** Storage account / File share for you,
go directly to [mounting](#mount-storage). Do not use another person's share or a HOME image for another purpose.
For self-creation, follow these steps.

### Create a Storage account

1. Sign in to [Azure Portal](https://portal.azure.com/).
2. Search for **Storage accounts**, then select **Create**.
3. Under **Basics**, set:

   | Field | Setting |
   |---|---|
   | **Subscription** | Recorded subscription |
   | **Resource group** | Assigned **existing RG**; do not use **Create new** |
   | **Storage account name** | Recorded unique name dedicated to you; if taken, choose an unused name and update your record |
   | **Region** | Match the supported Cloud Shell location you will select; do not simply reuse the RG region |
   | **Primary service** | `Other (tables and queues)` |
   | **Performance** | `Standard`, with `general-purpose v2 account` in its description |
   | **Redundancy** | `Locally-redundant storage (LRS)` |

4. **Primary service** does not restrict available storage types.
   `Other (tables and queues)` still allows Azure Files shares after creation.
   **Do not select Azure Files as Primary service in this procedure.**
   In the 2026-09-09 Portal UI, that selection was observed to change Review to
   **Account type: File shares**, **Media Tier: HDD**, **Provisioned v2**,
   even after selecting Standard.
5. Keep organization-approved Cloud Shell-compatible security/network settings.
   Do not weaken secure transfer, TLS 1.2+, or SMB encryption in transit;
   do not enable anonymous Blob access.
   If shared-key standard mounts are not clearly permitted, or network/policy blocks occur,
   contact the administrator rather than removing restrictions.
6. In **Review + create**, recheck subscription, existing RG, name, and matching region.
   Open **View automation template > Parameters** and verify
   **`kind=StorageV2`, `accountType=Standard_LRS`** without editing values/templates.
   The 2026-09-09 UI was observed to show **Account type: Page blobs** in Review
   even with correct Other / Standard selections.
   Use **ARM template kind / accountType**, not Review description labels, as evidence.
   If different, do not create; return to **Basics** and select again.
   If StorageV2 / Standard_LRS cannot be confirmed, consult the administrator;
   do not substitute `FileStorage` or Premium.
7. After confirming the configuration, select **Create**, then **Go to resource**.
   Read-only checks after Cloud Shell connection also verify actual kind / SKU / provisioning state.

Do not copy the main Terraform management tags to this storage.
Storage is an execution prerequisite, managed separately from the workload created/deleted by `setup.sh` / `destroy.sh`.
No **Access keys** display or key/SAS copying is needed.

### Create an Azure Files share

1. Open the account's **Data storage > Classic file shares**, not Blob containers.
2. Select **New classic file share** and enter your recorded **Name**, for example `cloudshell-handson`.
   Use lowercase letters/numbers and single hyphens; begin/end with a letter or number.
3. Choose **Access tier = Transaction optimized**. StorageV2 pay-as-you-go shares use SMB.
   Do not choose NFS or another file-share resource provider.
4. Check **Backup**. **Enable backup** defaults On and configures a new Recovery Services vault
   and backup policy. If optional for this new workshop-only share, uncheck it to avoid extra resources.
   **Do not change required organizational backups or existing protection**; coordinate separately if necessary.
5. In **Review + create**, verify recorded **Name**, **Access Tier = TransactionOptimized**,
   **Protocol = SMB**, and **no new Vault / backup policy creation**.
   If a vault remains, return to **Backup**; consult the administrator if mandatory.
   Confirm the configuration, select **Create**, and verify your share in the list.
6. Record subscription / RG / Storage account / File share and newly created targets.
   If setting a quota, confirm capacity for the HOME image, materials, and dependencies with the administrator.

</details>

<a id="mount-storage"></a>

## 3. Verify persistent storage and Bash

After automatic creation, check the Bash prompt and **Manage files > Open file share** target.
Do not switch to a storage-free **No storage account required** session.

<details>
<summary>Existing Storage only: explicitly select and mount it</summary>

1. Open **Cloud Shell** in Azure Portal.
2. Select **Bash**.
3. Under **Getting started > Mount storage account**, choose the subscription and **Apply**.
4. Select **Select existing storage account > Next**.
5. Select recorded **Resource group**, **Storage account name**, and **File share**, then **Select**.
6. Verify the Bash prompt and the target in **Manage files > Open file share** agree.

</details>

For manually created Storage, also use this **read-only** check:
verify `kind = StorageV2`, `sku = Standard_LRS`, and `provisioningState = Succeeded`.

```bash
az storage account show \
  --subscription "<subscription-id>" \
  --resource-group "<resource-group>" \
  --name "<storage-account-name>" \
  --query "{kind:kind, sku:sku.name, provisioningState:provisioningState}" -o table
```

**A Bash prompt alone does not prove a persistent mount.**
The command verifies Storage account creation, not HOME persistence.
An old share reference can fail to mount and leave an ephemeral session.
Do not continue; preserve original settings/storage and check explicit reconfiguration below.

<details>
<summary>Existing Cloud Shell users only: check the current connection</summary>

If already connected to your recorded workshop share, use it without resetting settings.
If connected to storage for another purpose, do not begin or switch without permission.
Record original `preferredLocation`, subscription / RG / account / share, and personal settings;
preserve running work/files and review switching impact with the instructor/administrator.
Do not delete an old share outside the assigned RG just because mounting failed.

Use **Settings > Reset User Settings** only if connection selection must be repeated
(for example, a previous **No storage account required** selection or an ephemeral session after a failed mount),
and you understand and approve the impact.
Confirming **Reset** resets the current session/personal settings.
Unsaved files and processes are lost, so save first.
The original Azure Files share is not deleted; a new share uses a different HOME image.
Repeat **Mount storage account** in this section and match Cloud Shell location to the new storage region.
Preserve original settings to discuss whether they must later be restored.

**Reset User Settings is not standard reconnection or cleanup.**
Do not automatically delete/reset old settings or storage used for other purposes.

</details>

### Verify the storage location

Cloud Shell can save a HOME disk image in Azure Files and mount the share at `$HOME/clouddrive`.
Put the repository and `.venv` **inside HOME**, where Unix links and permissions work.
**Do not clone or create venvs directly in the `clouddrive` SMB share.**

```bash
printf 'HOME=%s\n' "$HOME"
findmnt -T "$HOME"
findmnt -T "$HOME/clouddrive"
df -h "$HOME" "$HOME/clouddrive"
```

The existence of a `clouddrive` directory alone does not prove persistence.
In addition to script mount checks, perform the [actual restart check](#persistence).
HOME images in `.cloudconsole`, Terraform state, and Azure CLI caches are sensitive.
Do not broaden share access or distribute the whole HOME directory.

<a id="setup"></a>

## 4. Prepare materials and tools

In Cloud Shell Bash, substitute the instructor-provided URL and branch.
`<...>` values are placeholders, not literal inputs.

```bash
git clone --branch "<workshop-branch>" --single-branch \
  "<public-repository-https-url>" "$HOME/foundry-agent-service-handson"
cd "$HOME/foundry-agent-service-handson"
bash scripts/setup-cloud-shell.sh
source scripts/activate-cloud-shell.sh
```

If the directory already exists, do not overwrite/delete/reclone it.
Verify it is the original workshop repository and [resume](#resume).
`setup-cloud-shell.sh` prepares tools; it is separate from workload `setup.sh`.
It does not modify system Python / Azure CLI, and reuses an available Python 3.13.
Otherwise it installs an official standalone CPython distribution, also used by uv, in user-owned storage.
The script manages versions, sources, and SHA-256; participants do not change them.
If native Graphviz is missing, it uses a user-owned micromamba / conda-forge environment.
`pip install graphviz` alone is not a native renderer.
It checks at least 3 GiB free HOME space initially, or 512 MiB when rechecking an existing setup.
If insufficient, consult the administrator rather than deleting unrelated files.

After successful preparation, check:

```bash
.venv/bin/python --version
src/hosted-agent/.venv/bin/python --version
.venv/bin/jupyter kernelspec list
dot -V
```

| Target | Expected |
|---|---|
| Root `.venv` | Python `3.13.x` for shared scripts, deployment, and JupyterLab |
| `src/hosted-agent/.venv` | Python `3.13.x` for Agent Framework Labs 7 / 8 |
| Kernels | `foundry-workshop` and `foundry-hosted-agent` |
| `dot` | Native Graphviz version displayed |

Root uses `azure-ai-projects==2.5.0`; Hosted Agent uses `<2.4`.
Do not combine the two `.venv` environments. Normal participation needs no configuration/source edits.
Report missing dependencies, capacity, or network errors to the instructor, resolve the cause,
then repeat the same preparation command.
Do not use `sudo`, `apt-get`, Docker daemon, or system-Python package installation.

`source scripts/activate-cloud-shell.sh` sets PATH and
`AZURE_TOKEN_CREDENTIALS=AzureCliCredential` **only for workshop processes launched from this Terminal**.
Repeat for each new Terminal/reconnection.
Do not copy this credential restriction to the Hosted deployment; Hosted runtime uses managed identity.

<a id="persistence"></a>

## 5. Verify persistence before creating Azure resources

**Do this before Lab 1's historical `setup.sh`.**
Official storage documentation and FAQ descriptions of HOME persistence differ;
do not assume files are saved based on documentation alone.

1. In the prepared repository, create a nonsecret check file:

   ```bash
   cd "$HOME/foundry-agent-service-handson"
   date -u '+%Y-%m-%dT%H:%M:%SZ' > cloud-shell-resume-check.txt
   cat cloud-shell-resume-check.txt
   ```

2. Record the timestamp and verify no other work is running.
3. Select toolbar **Restart** and wait for container restart.
   **New session** only starts another process in the same container and is not an equivalent test.
4. Return to Bash using the same recorded storage and check **before recloning or rerunning bootstrap**:

   ```bash
   cd "$HOME/foundry-agent-service-handson"
   cat cloud-shell-resume-check.txt
   test -f notebooks/07-agent-framework-harness.ipynb
   test -f notebooks/08-hosted-agent.ipynb
   source scripts/activate-cloud-shell.sh
   .venv/bin/python --version
   src/hosted-agent/.venv/bin/python --version
   .venv/bin/jupyter kernelspec list
   dot -V
   ```

5. If the timestamp, materials, both environments, and kernels remain, remove only the check file:

   ```bash
   rm cloud-shell-resume-check.txt
   ```

If anything is missing, stop and ask the administrator to inspect original share / HOME image and mount.
Do not create Azure resources with unverified persistence.
After historical Lab 1, reconnection must also retain the same state and `.workshop/context.json`.

<a id="authentication"></a>

## 6. Check Azure CLI sign-in

Use Cloud Shell's existing Azure CLI sign-in and explicitly select the assigned subscription:

```bash
az account set --subscription "<subscription-id>"
az account show --query "{subscriptionId:id, user:user.name}" -o table
```

Verify the displayed user is the person assigned RG Owner.
If Foundry / Search operations report `Audience ... is not a supported MSI token audience`,
use the official FAQ recovery steps, then retry the original operation:

```bash
az login --use-device-code
az account set --subscription "<subscription-id>"
```

If device-code authentication is prohibited, stop and consult the administrator.
Do not share device codes, tokens, or Storage keys.
No API key/client-secret substitution or additional `azd auth login` is required.

<a id="jupyter"></a>

## 7. Open JupyterLab through Web preview

Use two Cloud Shell Terminals. Keep Jupyter running in **Terminal A** and enter lab commands
in **Terminal B**. These are not PC PowerShell steps.

1. In Terminal A, enter the repository root and run this **single startup command**.
   It prepares dependencies initially and checks/reuses them later:

   ```bash
   cd "$HOME/foundry-agent-service-handson"
   bash scripts/start-cloud-shell-jupyter.sh
   ```

2. Enter a Jupyter-specific password of at least 12 characters twice.
   Input is hidden; use the same password for browser login in this session.
3. When `Open Cloud Shell Web preview for port 5000` appears, open toolbar **Web preview**
   and enter port **5000**. Use **Open and browse** for a new tab.
   If you selected **Open port** first, use **Preview port 5000** from the menu.
   If Web preview is absent, check **More commands**.
   Supported ports are `1025–8079` or `8091–49151`.
4. The preview tab sends its actual HTTPS URL to a temporary discovery server
   and reloads automatically after JupyterLab starts.
   No URL copying, Ctrl+C in Terminal A, or second startup command is needed.
5. At Jupyter login, enter the step 2 password.
   Startup serves files only from the repository and restricts access to the actual preview origin.
   An internal token is also stored in a user-only file, never logged.
   Do not disable token authentication/XSRF or allow every Origin.
6. Open Terminal B with toolbar **New session**.
   It connects to the **same container**, but environment variables are separate, so run:

   ```bash
   cd "$HOME/foundry-agent-service-handson"
   source scripts/activate-cloud-shell.sh
   ```

If the port is occupied, do not silently change ports; check your existing Jupyter process.
Save and shut down an unneeded server normally; do not stop others' or unrelated processes.
Default listening is `127.0.0.1`. Only if the instructor confirms Cloud Shell proxy cannot reach
loopback, explicitly use `--listen 0.0.0.0` for **both** discovery and Jupyter startup.
Keep authentication and actual-preview-origin restrictions.
Use `--base-url` only after the instructor confirms the actual URL and proxy forwarding;
do not guess values.
For continuing authentication/proxy/WebSocket errors, keep protections and consult
[troubleshooting](../troubleshooting.md). The historical Cloud Shell subsection is no longer current.

<details>
<summary>Only if automatic preview detection fails: manual discovery</summary>

Use the former two-stage mode to determine the actual URL:

```bash
bash scripts/start-cloud-shell-jupyter.sh --discover-preview --port 5000
```

Open port 5000 through Web preview, record the displayed actual HTTPS URL, then stop with Ctrl+C.

```bash
bash scripts/start-cloud-shell-jupyter.sh \
  --port 5000 \
  --preview-url "<actual-https-preview-url>"
```

Include no query, fragment, or token in the URL. Authentication and XSRF remain enabled.

</details>

### Cloud Shell relay compatibility

Unlike ordinary Jupyter, Cloud Shell relay does not forward URL prefixes, redirects,
HTTP status, cookies, and browser WebSockets unchanged.
Startup applies compatibility behavior only in this environment.
Only after verifying the Jupyter password does it bind a Jupyter session to Azure's existing
Secure / HttpOnly relay cookie. It does not copy authentication cookies/tokens to JavaScript or URLs.
Only readable `_xsrf` is set from the login form, preserving XSRF checks on changes.

Kernel communication uses HTTP polling with authentication, XSRF, and user isolation,
connecting to a loopback WebSocket inside Cloud Shell.
It is not a direct browser WebSocket connection and does not change Codespaces behavior.
Server-side channels/queues have limits and expiry; logout/shutdown requires reauthentication.

<a id="notebook"></a>

## Notebook operations

If Cloud Shell ended during Portal-focused Labs 2–6, first [reconnect](#resume)
and restart Jupyter in the same environment.
Verify the JupyterLab file browser opens the repository root.
The shared notebooks are `notebooks/07-agent-framework-harness.ipynb` and `notebooks/08-hosted-agent.ipynb`.
Here, verify opening and kernels only; run Azure-calling learning cells in their respective labs.

For first connection checks, use **File > New > Console**, select
**Python (Foundry Workshop)** and **Python (Foundry Hosted Agent)** one at a time,
and run this in each with **Shift+Enter**, without Azure calls:

```python
import sys
print(sys.version)
print(sys.executable)
```

Both should show Python `3.13.x`, with root `.venv/bin/python` and
`src/hosted-agent/.venv/bin/python`, respectively, proving both kernels connect and execute.
End each check Console with **Kernel > Shut Down Kernel**, then close it.
No extra check cells need to be added to main notebooks.

1. Double-click the lab's `.ipynb`.
2. Use the kernel dialog, top-right kernel name, or **Kernel > Change Kernel…**
   to select **Python (Foundry Hosted Agent)**.
3. Labs 7 / 8 use `src/hosted-agent/.venv/bin/python`.
   Root **Python (Foundry Workshop)** is for Lab 4's optional SDK notebook,
   not Agent Framework exercises.
4. Run one selected cell at a time with **Run** or **Shift+Enter**, then **Save**.
   In visualization cells, verify Graphviz renders the actual SVG.

If additional notebook packages are needed, use `%pip` for the current kernel, not `!pip`.
Normally no installation is needed; startup prepares fixed dependencies.

Kernel names are `foundry-hosted-agent` / `foundry-workshop`.
Displaying a notebook in the browser is insufficient; the connection-check cell must execute.
Repair kernel, saving, or rendering problems before continuing.
In this historical procedure, Lab 8 **Run All** did not deploy; deployment used the shared lab's Terminal command.

**For environment preparation, return to [current Lab 1](../../../labs/01-setup.md);
the historical step 2 preflight procedure is no longer available.**
If coming from Labs 7 / 8, resume the same notebook exercise there.

<a id="files"></a>

## Download Lab 4 materials to your PC

Cloud Shell / JupyterLab and your PC have separate filesystems.
Foundry Portal **Upload skill** selects PC files.
Although `.workshop` is hidden, JupyterLab need not display all hidden files.

1. After generating historical Lab 4 materials, in connected Terminal B,
   display HOME-relative paths for **only the two named ZIPs**:

   ```bash
   cd "$HOME/foundry-agent-service-handson"
   realpath --relative-to="$HOME" \
     .workshop/toolbox/travel-estimation.zip \
     .workshop/toolbox/preapproval-simulation.zip
   ```

2. Select toolbar **Manage files > Download**.
3. Verify the field prefix is `/home/<your-user-name>/` and paste a **HOME-relative path**
   such as `foundry-agent-service-handson/.workshop/toolbox/travel-estimation.zip`,
   then **Download**.
   Even if described as “fully qualified file path”, an absolute path after that prefix
   duplicates HOME and causes `Could not download, try again.`
   Use a full absolute path only in UIs without a prefix.
   `~`, `$HOME`, and `$PWD` are not expanded in the field.
4. Select the **ZIP filename link** in the **Download file** notification to save to PC.
   The first **Download** alone is insufficient; distinguish this from a same-named file-explorer item.
   Repeat for `preapproval-simulation.zip` and verify both on your PC.
5. In Foundry Portal **Upload skill**, select the corresponding PC ZIP.
   Do not extract/recompress generated ZIPs; `SKILL.md` is at the root.

Display OpenAPI with historical `cat .workshop/toolbox/travel-ops.openapi.json` and paste it.
Do not download all `.workshop`, Terraform state, HOME images, Jupyter runtime, or authentication files.
Download saved notebooks individually using the same prefix/relative-path relationship.

To upload a PC file to Cloud Shell, use **Manage files > Upload**.
This places a file in HOME; it is not Foundry Portal Skill registration.
Use step 4 clone for public workshop materials; do not import `.git`, `.venv`, state, or credentials.

<a id="resume"></a>

## Resume after interruption or reconnection

Save notebooks at suitable checkpoints because Cloud Shell **may end after 20 minutes of inactivity**.
Saving preserves cells/outputs, not Python variables, AgentSession, todos, memory, or running Jupyter processes.
Do not use infinite keepalive. During Portal-focused Labs 2–6, save check notebooks and shut down Jupyter normally.
For `Directory not found` or download failures on resume, check Cloud Shell disconnection first.
Close expired preview tabs, reconnect to the same storage, verify state, then retry.

1. Open Cloud Shell **Bash** from Azure Portal.
   If prompted, select the recorded **same subscription / account / share**.
   Do not switch to a new share or HOME image.
2. Enter and activate the original repository:

   ```bash
   cd "$HOME/foundry-agent-service-handson"
   source scripts/activate-cloud-shell.sh
   az account set --subscription "<subscription-id>"
   az account show --query "{subscriptionId:id, user:user.name}" -o table
   ```

3. If historical Lab 1 provisioning completed, verify original `.workshop/context.json`
   and Terraform state remain. Check existence without publishing or screen-sharing contents.
   If missing, do not start setup in another state; check original storage/HOME mount with the instructor.
   For interrupted setup, preserve `.workshop/terraform-inputs.json` and original state while resuming.
4. Repeat the one-command [Jupyter startup](#jupyter).
   The preview tab automatically discovers the new session's actual preview URL.
   If an existing server remains in the same container, inspect it rather than starting a duplicate.
5. Open the same saved notebook and select **Python (Foundry Hosted Agent)**.
   Rerun required cells from connection and Agent/workflow construction in order.
   Recheck Lab 7's plan; old output does not mean the running session was restored.
6. If waiting for evaluation or remote build, check existing run/version status in the Portal first.
   Azure processing may still be running or completed; do not submit duplicate evaluation/deployment.

No bootstrap rerun is needed if dependencies are healthy.
Only when necessary, rerun `setup-cloud-shell.sh` in the same repository.
Do not recover by deleting existing files or user settings.

<a id="stop"></a>

## Finish after Lab 9 and delete dedicated storage

**Order: successful workload destroy → download results → stop Jupyter →
close Web preview → exit Cloud Shell → delete only newly created dedicated storage.**

1. In the historical [Lab 9](../../../labs/09-observability-cleanup.md) workflow,
   verify shared `./scripts/destroy.sh` succeeded and no Terraform/SDK-managed workshop resources remained.
   **Leave the RG itself.** If unsuccessful, do not delete storage; preserve state and `.workshop`.
   The linked current Lab 9 instead deletes the dedicated workload RG.
2. **Save** needed notebooks and download only safe results via [Manage files > Download](#files).
   Verify PC copies. Do not distribute or include Terraform state, credentials, Jupyter runtime,
   or the whole HOME directory as evidence.
3. Select JupyterLab **File > Shut Down**, or press **Ctrl+C** in Terminal A
   and confirm shutdown. Verify your Jupyter ends and Bash prompt returns.
4. Select Cloud Shell **Web preview > Close port 5000** and close the preview tab.
5. Run `exit` in **every session opened with New session**, including Terminals B and A.
   Sessions are independent; closing one does not end all.
6. Use **Settings > Reset User Settings**, or administrator-approved unmounting,
   to detach this share. This ends the session but does not delete Storage.
7. In Azure Portal, open the **dedicated RG automatically created by Cloud Shell** in step 2.
   Match subscription / RG / account / share and verify it is dedicated to this participant's Cloud Shell.
8. Verify no unrelated resources are present, select **Delete resource group**,
   check/enter the RG name, and delete. This removes the Storage account, share, and HOME image.
   **Historical `destroy.sh` did not delete the participant-created workload RG.**
9. Refresh both RGs. Verify Cloud Shell RG is gone and the workload RG/preexisting resources
   remain as expected for this historical procedure.

Do not delete administrator-assigned existing accounts.
If only a new share was created in existing Storage, confirm authorized scope with the administrator
and delete only your recorded share under **Classic file shares**.
Soft-delete/backup retention may retain data and charges. Do not disable protection to force deletion;
ask the administrator to confirm retention and completion.
Do not delete other users' shares or preexisting HOME images.

Storage deletion is not automatic in `destroy.sh`.
**Do not automatically reset existing Cloud Shell user settings.**
If deleted storage remains the next connection target, check your record and understand
[connection-switching impact](#mount-storage) before selecting new storage with the administrator.

## Official references

Retrieved: **2026-09-09**. These explain UI/constraints, not verified behavior in every tenant.
Before an event, instructors must use an actual browser to verify authentication, cell execution,
saving, Graphviz, post-restart persistence, and cleanup.

- [Cloud Shell toolbar, Manage files, New session, Web preview](https://learn.microsoft.com/azure/cloud-shell/use-the-shell-window)
- [Automatically create new Cloud Shell Storage](https://learn.microsoft.com/azure/cloud-shell/get-started/new-storage)
- [Mount existing storage](https://learn.microsoft.com/azure/cloud-shell/get-started/existing-storage)
- [HOME disk images and Azure Files persistence](https://learn.microsoft.com/azure/cloud-shell/persisting-shell-storage)
- [FAQ: 20-minute inactivity, 20 concurrent users, sudo, authentication audience](https://learn.microsoft.com/azure/cloud-shell/faq-troubleshooting)
- [Create a Storage account](https://learn.microsoft.com/azure/storage/common/storage-account-create?tabs=azure-portal)
- [Create StorageV2 pay-as-you-go Azure Files shares](https://learn.microsoft.com/azure/storage/files/create-classic-file-share?tabs=azure-portal)
- [Jupyter Server security](https://jupyter-server.readthedocs.io/en/latest/operators/security.html)
<!-- historical-content:end -->
</details>
