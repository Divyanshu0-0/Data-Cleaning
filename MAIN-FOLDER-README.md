# Hero-AI-Projects

Owner: **Hero**
A collection of AI/ML learning projects and freelance/gig-ready deliverables.

This folder mixes two kinds of work:
- **Learning projects** — built while progressing through the AI/ML roadmap
  (EDA, model training, healthcare AI experiments, etc.)
- **Freelance/gig projects** — client-ready deliverables (scripts, demos,
  reports) meant to be reused or shown as portfolio samples on
  Fiverr/Upwork

---

## Folder structure

```
Hero-AI-Projects/
├── README.md                     <- this file
├── freelance-gigs/
│   ├── data-cleaning-automation/
│   │   ├── clean_data.py
│   │   ├── messy_sales_data.csv
│   │   ├── cleaned_sales_data.csv
│   │   ├── data_cleaning_report.txt
│   │   └── README.md
│   └── (future gigs go here, one subfolder each)
│
└── learning-projects/
    ├── titanic-eda/
    ├── blood-cancer-detection-pytorch/
    ├── histopathology-sklearn-pipeline/
    ├── medidiagnose-cms/
    └── (future learning projects go here, one subfolder each)
```

**Rule of thumb:** every project gets its own subfolder with its own
`README.md`. This top-level README only gives the map — details live inside
each project.

---

## Project index

Keep this table updated as new projects are added — it's the fastest way to
find something later.

### Freelance / Gig projects

| Project | Folder | Description | Status |
|---|---|---|---|
| Data Cleaning & Automation | `freelance-gigs/data-cleaning-automation/` | Reusable script to clean messy CSV/Excel files (dates, currency, duplicates, missing values) + before/after demo | ✅ Done |

### Learning projects

| Project | Folder | Description | Status |
|---|---|---|---|
| Titanic EDA | `learning-projects/titanic-eda/` | Exploratory data analysis with Pandas, Matplotlib, Seaborn | ✅ Done |
| Blood Cancer Detection | `learning-projects/blood-cancer-detection-pytorch/` | PyTorch, ResNet-50 backbone, attention gates, Macenko stain normalization, Grad-CAM | ✅ Done |
| Histopathology ML Pipeline | `learning-projects/histopathology-sklearn-pipeline/` | scikit-learn, 5 classifiers + ensemble on synthetic histopathology features | ✅ Done |
| MediDiagnose CMS | `learning-projects/medidiagnose-cms/` | Claude-API-powered prototype that analyzes patient reports (blood, X-ray, CT, MRI, ECG) with Hinglish UI | ✅ Prototype |

---

## Conventions used across projects

- Each project folder is **self-contained** — it should run on its own
  without depending on files from other project folders
- Each project has its **own README.md** explaining setup, usage, and any
  known limitations
- Freelance projects favor **generic, reusable, well-commented code** since
  they'll be reused across different clients
- Learning projects favor **documented experiments** — it's fine if these
  are messier, since the goal is understanding, not delivery

---

## Adding a new project

1. Create a subfolder under `freelance-gigs/` or `learning-projects/`
   (whichever fits)
2. Add a project-level `README.md` inside it
3. Add a row to the relevant table above in this file
