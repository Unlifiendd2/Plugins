from dotenv import load_dotenv
load_dotenv()

import torch
torch.set_num_threads(8)

"""
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("docling").setLevel(logging.DEBUG)
"""

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.models.factories import get_ocr_factory
from docling_core.types.doc import PictureItem
from docling.datamodel.accelerator_options import AcceleratorOptions
from docling_core.types.doc.document import PictureMeta
from docling_core.types.doc.document import DescriptionMetaField
import numpy as np
from pathlib import Path

_DO_OCR_ = True
_OCR_PICTURES_ = True

# Configuration des options
pipeline_options = PdfPipelineOptions()
if _DO_OCR_ :
    pipeline_options.images_scale = 1.0
    pipeline_options.do_ocr = True             # False si le PDF a déjà une couche texte
    pipeline_options.ocr_options.lang = ["fr", "en"]
    if _OCR_PICTURES_ :
        pipeline_options.generate_picture_images = True

# Création du convertisseur avec ces options
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options,
            backend=PyPdfiumDocumentBackend
        )
    }
)

# Conversion
doc = converter.convert("C:/Users/PaulinBlattmann/Downloads/Prez Arturia x Orkeer V2 (2023_09_04).pdf").document

# OCR les images pour annotation
def ocr_array(rgb, min_score=0.5):
    res = ocr_model._engine.reader(rgb)
    txts = getattr(res, "txts", None)
    scores = getattr(res, "scores", None)
    if not txts:
        return ""
    if scores:
        kept = [t for t, s in zip(txts, scores) if s >= min_score]
    else:
        kept = list(txts)
    return " ".join(kept)

if _DO_OCR_ and _OCR_PICTURES_ :
    ocr_factory = get_ocr_factory()
    ocr_model = ocr_factory.create_instance(
        options=pipeline_options.ocr_options,
        enabled=True,
        artifacts_path=None,
        accelerator_options=AcceleratorOptions(),
    )

    picture_ocr = {}
    for item, _level in doc.iterate_items():
        if not isinstance(item, PictureItem):
            continue
        pil_img = item.get_image(doc)          # PIL.Image of the cropped picture
        if pil_img is None:
            continue

        rgb = np.array(pil_img.convert("RGB"))
        try:
            text = ocr_array(rgb)   # returns list of cells with .text
            text = " ".join(text.split())
        except Exception as e:
            text = ""
            print(f"OCR failed on {item.self_ref}: {e}")

        # Inline le OCR
        if text:
            # picture_ocr[item.self_ref] = text
            item.meta = PictureMeta(description=DescriptionMetaField(text=text))


# Export markdown
markdown_content = doc.export_to_markdown()

# Save to file
output_md = Path("C:/Users/PaulinBlattmann/Documents/Chroma/output/propale_Arturia.md")
output_md.write_text(markdown_content, "utf-16")
print(f"\nFull markdown saved to: {output_md}")

