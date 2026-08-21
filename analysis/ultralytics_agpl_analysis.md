# D-1 Training-Stack License Analysis — Ultralytics AGPL-3.0 Caveat

**Author:** Thermal Surveillance Drone agent
**Date:** 2026-08-15
**Status:** Analysis complete; decision needed from David
**References:** `model.sysml` line 864 (`license = "project-developed (AGPL training-stack caveat)"`), TASKS.md D1.9

---

## 1. The Problem

The D-1 thermal detection/classification model needs a training stack. The natural choice is **Ultralytics YOLO** (YOLOv8 / YOLO11): it is the most widely used framework, has the richest documentation, and the project's existing tooling pipeline (`src/train.py`) is already written against it. However, Ultralytics YOLO is licensed under **AGPL-3.0**, a strong copyleft license with obligations that reach into downstream projects.

The current model entry in `model.sysml` flags this with a caveat but has never analyzed what it actually means for this project.

## 2. How AGPL-3.0 Applies Here

### 2.1 What the License Says (from ultralytics.com/license)

Ultralytics explicitly states that **all** of the following triggers require an Enterprise License (not just AGPL compliance):

- **Commercial products or services** (the drone system, if deployed in a commercial context)
- **Embedded deployments in hardware, edge devices, robotics, cameras, or appliances** ← direct hit
- **Internal business tools or private company applications**
- **SaaS platforms, APIs, or cloud systems** (AGPL §13 — the "SaaS loophole" closer)
- **Using custom-trained or fine-tuned models in a proprietary or commercial setting**

The license covers not just the repository code, but **models trained with that code** — Ultralytics treats fine-tuned weights as derivative works under AGPL.

### 2.2 What AGPL Compliance Means

If you use Ultralytics code or weights under AGPL-3.0 (without buying an Enterprise License), you must:

1. **Include the AGPL-3.0 license notice** in your project distribution
2. **Provide complete corresponding source code** of the entire combined work — this means:
   - The training pipeline (which is already open-source)
   - The mission application (D-2) — **this is the problem**: AGPL's copyleft can reach into the larger program that *uses* the model
   - The systemd service layer, config files, everything
3. **For network-interactive programs** (§13): if users interact with the program over a network (e.g., a GCS operator sending commands to the drone which runs the AGPL-covered model), you must offer them the source — even though you never shipped them a binary

### 2.3 Why It Probably Doesn't Trigger Here

This project is a **personal, non-commercial hobby/surveillance system**. Key defenses:

- **No distribution.** The drone is built and flown by David. It is not sold, not shipped as a product, not provided as a service. AGPL's distribution/conveying trigger (core obligation) never fires.
- **Not a SaaS product.** The only network interaction is the operator's GCS — a single-user MAVLink connection. This is not a "public-facing service" under §13.
- **No downstream recipients.** The source code is already on a public GitHub repo under project-developed license. AGPL-3.0 requires *license compatibility* with any copyleft library you incorporate, but since the whole repo is effectively open-source already (your choice), the copyleft reach doesn't add practical harm.
- **Non-commercial use.** Ultralytics's own FAQ explicitly says "Personal projects, learning, and experimentation" are covered by AGPL without needing an Enterprise License.

**Bottom line: For the project as currently scoped (personal, non-commercial, no distribution), AGPL-3.0 compliance is achievable at zero cost** — the main requirement is ensuring the D-2 mission application source is publicly available alongside the model, which it already is (GitHub).

## 3. What Changes If The Project Goes Commercial

If David ever:
- Sells the drone or the detection system
- Deploys it for paid wildlife surveys
- Shares it as a product or service to a client
- Uses it for a business's internal operations (e.g., a farm doing paid crop monitoring)

Then an **Ultralytics Enterprise License** would be needed. Pricing is not publicly disclosed (custom quote), but references suggest it is in the **$1,500–$5,000+/year** range depending on deployment scale. That's a non-trivial expense on a $2,500 total system budget.

## 4. Alternatives — Permissively Licensed Detection Frameworks

If David wants zero licensing uncertainty, these alternatives avoid copyleft entirely:

| Framework | License | YOLO Arch | Edge Export | Notes |
|-----------|---------|-----------|-------------|-------|
| **LibreYOLO** | MIT | YOLO9, RF-DETR, D-FINE | ONNX, TensorRT, RKNN via ONNX | Drop-in Ultralytics replacement; MIT-licensed; **recommended for AGPL avoidance** |
| **YOLOX** | Apache-2.0 | Anchor-free YOLO | ONNX → RKNN | Well-proven, large install base; install is finicky |
| **RT-DETR** (v1–v4) | Apache-2.0 | Real-time DETR | ONNX, TensorRT | Transformer detector, very good accuracy |
| **RF-DETR** | Apache-2.0 | Real-time DETR | ONNX, TFLite, TensorRT | Production-focused; strong perf |
| **PP-YOLOE** | Apache-2.0 | PP-YOLO | ONNX → RKNN | Baidu PaddlePaddle, slightly different ecosystem |
| **DAMO-YOLO** | Apache-2.0 | NAS-based YOLO | ONNX | Alibaba; less active maintenance |
| **YOLOv6** | MIT | YOLOv6 | ONNX | Meituan; older, but MIT |

All of these export to ONNX, which can then be converted to RKNN for the NanoPi M5's NPU — same pipeline as Ultralytics.

### 4.1 Cost of Switching

- **Training pipeline:** `src/train.py` uses the Ultralytics API (`YOLO()`). Switching to LibreYOLO would be a ~small code change (same API pattern). Switching to YOLOX or RT-DETR would require rewriting the training loop.
- **Model conversion:** The ONNX→RKNN conversion script (`conversion/to_rknn.py`) is model-format agnostic — it just needs an exported ONNX graph. No change needed regardless of training framework.
- **Inference wrapper (D2.6):** The RKNN wrapper implements a `Detector` interface. The caller (D-2 mission app) doesn't care which training framework produced the `.rknn`. No change needed.
- **Dataset/labels:** YOLO-format datasets are universal. All alternatives accept the same label format.

### 4.2 Recommendation

**Short-term (personal build): Stay on Ultralytics YOLO.** AGPL compliance is straightforward for a personal non-commercial project with public source code. The training pipeline `src/train.py` is already written for it; there is no reason to rewrite before the model even exists.

**If any commercial/revenue-generating use is planned:** Switch to LibreYOLO (MIT) or RF-DETR (Apache-2.0) at the training stage. The cost of switching goes up once training, hyperparameters, and augmentation pipelines are tuned — better to decide the license posture **before** D1.4 (training).

**Trigger for revisiting this decision:** Any of:
- David uses the drone for paid work
- The project is open-sourced beyond its current limited GitHub audience
- A third party expresses interest in using/deploying it
- David hires an employee or contractor who touches the model training code

## 5. Practical AGPL-Compliance Checklist (for the Personal Build)

If David stays on Ultralytics:

1. ✅ **Add AGPL-3.0 license text** to the repo root (a `LICENSE` file or a note linking to `https://www.gnu.org/licenses/agpl-3.0.html`)
2. ✅ **Add an AGPL notice** to the D-1 code and the D-2 mission app main source files — a comment block with the copyright line and a pointer to the license
3. ⬜ **Verify the D-2 mission app source is on GitHub alongside the model pipeline** (it already is, in the sibling DroneMissionApp repo, but confirm it's publicly accessible)
4. ✅ **No additional action needed** — the training code, the model weights, and the mission app are already built with open-source tooling and publicly available

## 6. Decision Record

| Option | Cost | Effort | Risk | Best For |
|--------|------|--------|------|----------|
| **A. Stay on Ultralytics AGPL** | $0 | ~1 h (add notice) | None for personal use | Current scope |
| **B. Switch to LibreYOLO (MIT)** | $0 | ~4 h rewrite training | None | Commercial future-proofing |
| **C. Buy Enterprise License** | ~$1,500–5,000/yr | ~30 min | Cost | Business deployment |
| **D. YOLOX / RF-DETR (Apache-2.0)** | $0 | ~12 h rewrite + retrain | None; more engineering | If DAVID prefers Apache-2.0 |

**David's choice needed at the [`SELECTED_COMPONENTS.md`](../SELECTED_COMPONENTS.md) level:** once picked, update `model.sysml` line 864's `license` field and the D-1 training pipeline's dependencies accordingly.

---

*This is an analysis briefing, not legal advice. License terms can change. Confirm any material decision with a qualified IP attorney before entering a commercial arrangement.*