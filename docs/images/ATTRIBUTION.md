# Image and icon attribution

Microsoft and Azure product names / logo trademarks belong to Microsoft.
Their use in these materials does not imply Microsoft endorsement.

## Microsoft Learn images

The following screenshot is included under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

| Workshop image | Microsoft Learn source | Changes |
|---|---|---|
| `lab09-delete-resource-group.png` | [Common resource group deletion procedure](https://github.com/MicrosoftDocs/azure-docs/blob/main/includes/alt-delete-resource-group.md) | None |

This is a generic resource group deletion example, not proof of workshop cleanup.

## Workshop Portal screenshots

| Workshop image | Captured screen | Changes |
|---|---|---|
| `lab01-template-succeeded.png` | Azure Portal deployment Overview: Your deployment is complete | Cropped; deployment, subscription, RG, time, and correlation information masked; completion display highlighted |

This real screenshot was captured during a previous deployment and illustrates
the Portal completion display. It is not evidence that the current GitHub /
Codespaces revision was deployed or validated.
Existing screenshots may show older UI or Japanese content; they are illustrative,
not proof of the current English revision's successful operation.
Screenshots are unchanged by the English diagram translation; no generated
illustration or translated diagram is presented as a captured product screen.

## Architecture diagrams

`azure-architecture-01.png` and `azure-architecture-02.png` were created for these materials.
The [editable PowerPoint](../diagrams/azure-architecture.pptx) is rendered with desktop PowerPoint.
The [overview JSON](../diagrams/azure-architecture.json),
[deployment / initialization JSON](../diagrams/azure-architecture-deployment.json),
and [SVG sources / hashes](../diagrams/azure-icons/manifest.json) are retained as
diagram specifications and provenance.

The English-label update translates the corresponding JSON specifications and
the existing native PPTX text shapes and speaker notes. Desktop PowerPoint COM
automation preserves the service objects, connections, and icons and exports the
two PNGs at 1800 × 1160 pixels. This is native diagram editing and PNG export,
not screenshot fabrication or evidence of English-release deployment.
See [diagram editing](../development/architecture.md#editing-architecture-diagrams)
for the supported manual / automation maintenance path.

| Icon collection | Version | Icons used |
|---|---|---|
| [Azure architecture icons](https://learn.microsoft.com/azure/architecture/icons/) | Azure Public Service Icons V24, July 2026; retrieved 2026-09-19 | Foundry Agent Service, Foundry IQ, Foundry Project, Foundry Models, Azure AI Search, Container Apps, Application Insights, Log Analytics, browser, template, resource group |

Microsoft permits icon use in architecture diagrams, training materials, and
documentation under the linked conditions. Original SVG contents are embedded
unchanged and displayed with their aspect ratios preserved.
The diagrams are not Microsoft reference architectures, product screenshots,
endorsements, or deployment evidence. Participant, Toolbox, initialization, and
completion-output symbols are generic PowerPoint shapes, not product logos.

Old `azure-architecture.svg` and [draw.io data](../diagrams/azure-architecture.drawio)
are historical artifacts from before the update. In addition to Azure Public
Service Icons V24, they use the Microsoft Entra ID icon from
[Microsoft Entra architecture icons](https://learn.microsoft.com/entra/architecture/architecture-icons)
(October 2023).

`workshop-architecture.svg` and `workshop-learning-flow.svg` are also workshop-specific
illustrations. Editable `.excalidraw` files are retained; distinguish these diagrams
from product screens or execution evidence.
