import os

# Extracted from the user's provided directory tree
tutorials_by_path = {
    "basics": [
        "01_BlocksAndFields",
        "02_Sweeps",
        "03_GameOfLife"
    ],
    "codegen": [
        "01_CodegenHeatEquation",
        "02_LBMLatticeModelGeneration",
        "03_AdvancedLBMCodegen",
        "04_LBComplexGeometry"
    ],
    "gpu": [
        "01_GameOfLife_cuda"
    ],
    "lbm": [
        "01_BasicLBM",
	"02_BasicLBM_ExemplaryExtensions",
	"03_LBLidDrivenCavity",
        "04_LBComplexGeometry",
	"05_BackwardFacingStep",
	"06_LBBoundaryCondition"
    ],
    "mesa_pd": [
        "01_MESAPD"
    ],
    "pde": [
        "01_SolvingPDE",
        "02_HeatEquation",
	"03_HeatEquation_Extensions"
    ]
}

# Base directory for documentation
base_dir = "tutorial_tracking"

# Markdown template
template = """# Tutorial {id} – {title}

## 1. Objective
Brief summary of what this tutorial demonstrates.

## 2. Configuration
- Build options enabled (`WALBERLA_BUILD_WITH_*`)
- Required CMake flags or modules
- Dependencies (e.g., Python, MPI, OpenMesh)

## 3. Source Files
- Main file: 
- Supporting files: 

## 4. Steps Taken
- Domain setup
- Field registration
- GUI usage (if any)

## 5. Observations / Output
- GUI screenshot or CLI output (if available)
- Field structure or block forest summary

## 6. Changes Made (if any)
- Code modifications
- Custom input parameters or configurations

## 7. Outcome / Key Takeaways
- What did you learn?
- Common pitfalls?
- How this links to future tutorials?

## 8. Questions or TODOs
- Remaining doubts?
- What should be tried next?
"""

# Generate folders and notes
for category, tutorials in tutorials_by_path.items():
    for tutorial in tutorials:
        folder_path = os.path.join(base_dir, category, tutorial)
        os.makedirs(os.path.join(folder_path, "screenshots"), exist_ok=True)
        notes_path = os.path.join(folder_path, "notes.md")
        with open(notes_path, "w") as f:
            f.write(template.format(id=tutorial, title=tutorial.replace("_", " ")))

"Tutorial tracking structure created with exact .dox case names."
