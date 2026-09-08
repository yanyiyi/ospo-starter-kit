# OSPO Starter Kit　Draft

This kit is a collection of templates for establishing an Open Source Program Office (OSPO) in an organization and for building the strategic use of open source together with an appropriate governance structure.

## ⚠️ Development Status and Roadmap

This kit is currently a **"draft (incomplete)"**. Some content is still under consideration or in progress and may change substantially. For the status of updates, see [Releases
](https://github.com/japan-opensource-hub/ospo-starter-kit/releases).

## Included Files and Overview

This kit contains the following documents.

### A. OSS Policy (Company-Wide Rules) Templates (`oss-policy-templates/`)

Templates that collect sample articles to refer to when drafting an internal OSS policy (company-wide rules), together with their background and customization guidance. Each article consists of three sections: "Sample Article", "Commentary", and "Customization Perspectives and Operational Notes".

- `introduction.md`: Introduction ─ How to Use This Document
- `articles/00_preamble.md`: Article 0. Preamble
- `articles/01_purpose.md`: Article 1. Purpose
- `articles/02_definitions.md`: Article 2. Definitions
- `articles/03_scope.md`: Article 3. Scope of Application
- `articles/04_ospo.md`: Article 4. OSPO
- `articles/05_oss_usage.md`: Article 5. OSS Usage
- `articles/06_contribution.md`: Article 6. Contribution to OSS Projects
- `articles/07_oss_release.md`: Article 7. Releasing Company Works as OSS
- `articles/08_personal_oss_activity.md`: Article 8. Employees' Personal OSS Activities
- `articles/09_trademark_and_brand.md`: Article 9. Handling of Trademarks and Branding
- `articles/10_license_violation_incident.md`: Article 10. Response to License Violations and Incidents
- `articles/11_security_and_vulnerability.md`: Article 11. Security and Vulnerability Management
- `articles/12_records_and_reporting.md`: Article 12. Records and Reporting
- `articles/13_education_and_awareness.md`: Article 13. Education and Awareness
- `articles/14_employment_rules_relation.md`: Article 14. Relation to Employment Regulations
- `articles/15_revision_and_enforcement.md`: Article 15. Revision and Enforcement


### B. Operation Templates (`operation-templates/`)

Document templates to publish on an internal portal (Wiki, SharePoint, and the like) and communicate to the people concerned. Each template carries a "Customization Checklist" and a "Customization Guide" (inside comments).

For how to introduce and customize the templates, see `how-to-use-templates-for-ospo.md` (for OSPO staff) and `how-to-use-guide-for-users.md` (for end users).

- **Fundamentals and Organization** (`about/`)
  - `opensource-guide.md`: [Company Name] Open Source Guide (entry point)
  - `about-opensource.md`: About Open Source
  - `benefits.md`: Benefits of Open Source
  - `ospo.md`: What Is an OSPO?
  - `innersource.md`: What Is InnerSource?
  - `glossary.md`: Glossary

- **License Compliance** (`compliance/`)
  - `license-compliance.md`: Open Source License Compliance
  - `what-is-a-license.md`: What Is a License?
  - `license-types.md`: Types of Licenses
  - `source-disclosure-licenses.md`: Licenses with Source Code Disclosure Obligations
  - `oss-with-commercial-license-options.md`: OSS with Commercial License Options
  - `license-faq.md`: License FAQ

- **Practice and OSS Utilization** (`using/`)
  - `using-oss.md`: Using Open Source
  - `finding-oss.md`: Finding Open Source Software
  - `oss-inventory.md`: Approved Internal OSS Inventory
  - `evaluation.md`: Evaluating Open Source Software
  - `supplier-procurement.md`: Procuring OSS from Suppliers
  - `usage-faq.md`: OSS Usage FAQ

## License

The text and documents contained in this kit are provided under **[CC0 1.0 Universal (Public Domain Dedication)](https://creativecommons.org/publicdomain/zero/1.0/)**.

- **Waiver of copyright**: Rights under copyright law are waived, so the content may be reproduced, modified, and redistributed without permission, whether for commercial or non-commercial purposes.
- **No attribution required**: There is no need to credit (attribute) the original authors. Feel free to rewrite the content and use it as an official internal document under your own brand and logo.

## Disclaimer (Notes on Use)

This kit may be used without copyright restrictions thanks to the CC0 license, but please keep the following in mind.

- **Legal review is necessary**: The policy and license explanations in this kit are generic templates. Before putting them into practice, always have them reviewed by your own legal or intellectual property department, or by an expert.
- **No warranty**: This kit is provided "as is", without any express or implied warranty, including warranties of merchantability, fitness for a particular purpose, and non-infringement. The providers accept no liability for any damages arising from the use of this kit.

## Contribution Guidelines (Provisional)

These will be updated as we go, but for the time being please use the following as a guide.

- For large structural or policy changes, please start a discussion in Issues first.
  - Examples: changes to the directory layout, substantial rewrites of a template, changes to operational rules, and so on.
  - When proposing an improvement, state the background and the effect you expect.
- Small fixes (typos, minor wording adjustments) can be sent straight as a Pull Request (hereafter "PR").
- In the title and description of a PR, please state as concisely as possible *why* the change is being made.
  - Prefixing commit titles with tags such as [add], [fix], or [update] is recommended.
- Handling PRs
  - A PR is merged after review by at least one person.
  - Automated reviews such as tests and linters must be passing.

## Response Targets (SLA: Service Level Agreement)

The maintainers handle Issues and Pull Requests using the following as a guide.

### Response Time Targets

- First response to an Issue
  - As a rule, a comment or a label **within one to two weeks**.
- Review of a Pull Request
  - As a rule, a review or a progress comment **within two weeks**.

The above are targets only and may slip depending on the season and circumstances.

### Scope of Response

The maintainers primarily handle items such as the following.

- Changes and improvements to the content or structure of the templates
- Unifying terminology and tidying up wording
- Adjustments to the overall direction and positioning of the OSPO Starter Kit

Conversely, the following are, as a rule, **outside the maintainers' SLA**.

- Individual consulting that goes into circumstances specific to a single organization
- Troubleshooting of system settings, networks, or authentication outside this repository
- Approval or authorization of company-wide systems and governance design other than the OSPO itself
- Anything else unrelated to the content of the templates

### Assumptions About Business Days and Hours

- Business days are assumed to be **weekdays (Japan time)**.
- During busy periods or while running events, responses may take longer than the targets above.

### Status of This SLA

- What is described here is only "the response the maintainers aim for"; it is not necessarily a legally binding service guarantee.
- The content of the SLA may be reviewed and updated according to actual operations and available resources.

## Publisher and Contact

For questions about the content of this kit, please contact the email address below.

Publisher: Information-technology Promotion Agency, Japan (IPA)

Contact: IPA Digital & AI Systems Design Center (DADC) disc-info@ipa.go.jp

## Production Team and Acknowledgements

The following members contributed as the core team in planning and creating this kit. Affiliations are those at the time the first (draft) edition was published.

- Planning: 今村 かずき (Software Engineering Group, Digital Engineering Department, IPA Digital Infrastructure Center)
- Writing: 服部 佑樹 (IPA Expert Member, GitHub Japan G.K.) / 渡邊 歩 (IPA Expert Member, Hitachi Solutions, Ltd.) / 福地 弘行 (Software Engineering Group, Digital Engineering Department, IPA Digital Infrastructure Center)
- Review: 大内 佳子 (Mitsubishi Electric Corporation) / 大和田 清志 (Socionext Inc.)

We also thank everyone on the teams that took part in the OSPO Level 1 workshop for their feedback.
