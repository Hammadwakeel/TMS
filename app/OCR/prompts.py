# app/OCR/prompts.py

# —————————————————————————————————————————
# 1) Prompt to Detect Document Type
# —————————————————————————————————————————
DOC_NAME_PROMPT = """
GOAL:
  Determine which of the supported document types the given image/page represents.

INSTRUCTION:
  You will be shown an image (or a single PDF page). It is exactly one of:
    • Commercial Driver’s License (CDL)
    • DOT Medical Card
    • Certificate of Insurance (COI)
    • Operating Authority (MC/DOT Certificate)
    • W-9 Tax Form
    • Broker Authority (FMCSA Certificate)
    • Surety Bond (BMC-84) or Trust Fund Agreement (BMC-85)

WARNINGS:
  – Do NOT output any additional words, punctuation, or formatting.
  – Do NOT quote the output.
  – Do NOT return JSON for this step.

OUTPUT STRUCTURE:
  Return exactly one of these lower‑case identifiers:
    cdl
    medical_card
    coi
    operating_authority
    w9
    broker_authority
    surety_bond
"""

# —————————————————————————————————————————
# 2) CDL Prompt
# —————————————————————————————————————————
CDL_PROMPT = """
GOAL:
  Extract every required field from a Commercial Driver’s License image.

INSTRUCTION:
  Analyze the image and locate each data element below. Preserve all original formats (dates, casing, punctuation).

WARNINGS:
  – Return ONLY the raw JSON object.  
  – Do NOT wrap it in code fences or add explanatory text.  
  – Do NOT omit any of the keys, even if a value is blank or “N/A.”

OUTPUT STRUCTURE:
  A JSON object with exactly these keys:
    {
      "name": string,               // full name on license
      "dob": string,                // date of birth
      "cdl_number": string,         // license number
      "state": string,              // state of issuance
      "issue_date": string,         // issue date
      "expiry_date": string,        // expiration date
      "license_class": string,      // class designation
      "endorsements": string,       // list/letters of endorsements
      "photo_present": boolean,     // true if photo visible
      "signature_present": boolean, // true if signature visible
      "mrz": string,                // machine-readable zone text or blank
      "security_features": string   // description of barcode/hologram/watermark
    }
"""

# —————————————————————————————————————————
# 3) Medical Card Prompt
# —————————————————————————————————————————
MEDICAL_CARD_PROMPT = """
GOAL:
  Extract key information from a DOT Medical Card image.

INSTRUCTION:
  Read all printed fields and capture exactly as they appear.

WARNINGS:
  – Do NOT include any commentary or section headers.  
  – Return raw JSON only, with all specified keys present.

OUTPUT STRUCTURE:
  {
    "name": string,                  // driver’s full name
    "dob": string,                   // date of birth
    "issue_date": string,            // certificate issue date
    "expiry_date": string,           // certificate expiration date
    "examiner_name": string,         // medical examiner’s name
    "examiner_license": string,      // examiner’s license number
    "examiner_signature": boolean,   // true if signature present
    "registry_number": string,       // national registry number or blank
    "card_type": string,             // type/class of certificate
    "restrictions": string           // any restrictions listed
  }
"""

# —————————————————————————————————————————
# 4) COI Prompt
# —————————————————————————————————————————
COI_PROMPT = """
GOAL:
  Extract structured insurance policy data from a Certificate of Liability Insurance (COI) document image.

INSTRUCTIONS:
  - Extract each field exactly as printed in the document.
  - Preserve formatting for names, addresses, monetary values (with commas and dollar signs), and dates (MM/DD/YYYY).
  - When multiple values exist for a field (e.g., insurers, NAIC numbers, policy numbers), return them as comma-separated strings in the order shown on the document.
  - All coverage types and their corresponding limits must be fully extracted and formatted exactly as printed.
  - If a value is missing or blank in the document (e.g., no dollar amount), do not include it in the final result.
  - Do not deduce or infer missing data — only extract what is visibly present.

STRICT RULES:
  – Do NOT summarize, reword, or paraphrase any text.
  – Do NOT include placeholders like “$” without values.
  – Provide only the final JSON object with no introductory or trailing text.
  – If a representative's signature or stamp is visible, set `"rep_signature": true`; otherwise, set it to false.

OUTPUT FORMAT:
Return only a valid JSON object in the following format:
{
  "carrier_name": string,               // Name of the producer or broker agency
  "carrier_address": string,            // Formatted address of the carrier
  "insurer_name": string,               // Comma-separated names of insurers A–F (in order)
  "naic_number": string,                // Comma-separated NAIC numbers (in same order as insurers)
  "policy_number": string,              // Comma-separated policy numbers
  "coverage_types": string,            // Comma-separated list of coverage types, exactly as printed
  "coverage_limits": string,           // Full list of limits with descriptions and values, comma-separated
  "effective_date": string,            // Primary policy effective date (MM/DD/YYYY)
  "expiration_date": string,           // Primary policy expiration date (MM/DD/YYYY)
  "certificate_holder": string,        // Full certificate holder block with line breaks
  "rep_signature": boolean             // true if a visible signature/stamp is present, else false
}
"""

# —————————————————————————————————————————
# 5) Operating Authority Prompt
# —————————————————————————————————————————
OPERATING_AUTHORITY_PROMPT = """
GOAL:
  Extract fields from an Operating Authority (MC/DOT Certificate) image.

INSTRUCTION:
  Capture all printed data, preserving numeric formats and labels.

WARNINGS:
  – Only return raw JSON.  
  – Do NOT include labels or units in values; include them only where part of printing.

OUTPUT STRUCTURE:
  {
    "carrier_name": string,
    "carrier_address": string,
    "mc_number": string,
    "dot_number": string,
    "authority_type": string,     // e.g., “common”, “contract”
    "issue_date": string,
    "expiration_date": string,
    "fmcsaseal_present": boolean
  }
"""

# —————————————————————————————————————————
# 6) W-9 Prompt
# —————————————————————————————————————————
W9_PROMPT = """
GOAL:
  Extract taxpayer information from a W‑9 Tax Form image.

INSTRUCTION:
  Read each field exactly; preserve line breaks in multiline addresses.

WARNINGS:
  – Return only JSON.  
  – Do NOT interpret business type codes; copy exactly as shown.

OUTPUT STRUCTURE:
  {
    "legal_name": string,
    "business_type": string,      // e.g., “LLC”, “Corporation”
    "tin": string,                // SSN or EIN
    "ein": string,                // repeated if applicable
    "signature_present": boolean,
    "date_signed": string
  }
"""

# —————————————————————————————————————————
# 7) Broker Authority Prompt
# —————————————————————————————————————————
BROKER_AUTHORITY_PROMPT = """
GOAL:
  Extract broker registration data from an FMCSA Broker Authority Certificate image.

INSTRUCTION:
  Capture exactly each printed item; do not reformat addresses.

WARNINGS:
  – Output raw JSON only.  
  – Do NOT add explanatory text.

OUTPUT STRUCTURE:
  {
    "broker_name": string,
    "broker_address": string,
    "mc_number": string,
    "authority_type": string,
    "issue_date": string,
    "expiration_date": string,
    "fmcsaseal_present": boolean
  }
"""

# —————————————————————————————————————————
# 8) Surety Bond Prompt
# —————————————————————————————————————————
SURETY_BOND_PROMPT = """
GOAL:
  Extract bond or trust agreement details from a Surety Bond (BMC-84/BMC-85) image.

INSTRUCTION:
  Read and record each field; preserve currency symbols and formatting.

WARNINGS:
  – Only return a JSON object.  
  – Do NOT include any extra keys.

OUTPUT STRUCTURE:
  {
    "broker_name": string,
    "bond_amount": string,           // include “$” if printed
    "surety_company": string,
    "bond_number": string,
    "effective_date": string,
    "expiration_date": string,
    "authorized_signatures": boolean
  }
"""
