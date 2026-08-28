"""Maps lesson slugs to devops_references keys for automatic appendix links."""

from __future__ import annotations

# lesson_slug -> tuple of keys in devops_references.REF_BY_KEY
LESSON_REF_KEYS: dict[str, tuple[str, ...]] = {
    # --- 30-day enterprise sprint (devops-interview-30-day) ---
    "30-day-battle-plan": ("interview", "master"),
    "linux-shell-interview": ("linux", "networking"),
    "git-collaboration-interview": ("git",),
    "networking-http-ops": ("networking", "aws"),
    "week1-checkpoint": ("linux", "networking", "interview"),
    "cicd-design-interview": ("cicd", "questions_cicd"),
    "cicd-release-engineering": ("cicd", "aws", "questions_cicd"),
    "docker-production-interview": ("docker", "kubernetes", "questions_k8s"),
    "kubernetes-production-essentials": ("kubernetes", "aws", "questions_k8s"),
    "week2-checkpoint": ("cicd", "docker", "interview"),
    "terraform-iac-interview": ("terraform", "aws"),
    "cloud-platform-engineering": ("aws", "kubernetes", "interview"),
    "config-secrets-twelve-factor": ("security", "aws"),
    "devsecops-supply-chain": ("security", "cicd"),
    "week3-checkpoint": ("terraform", "aws", "interview"),
    "observability-slo-interview": ("observability", "questions_sre"),
    "incident-response-interview": ("observability", "interview"),
    "behavioral-devops-interview": ("interview", "questions_behavioral"),
    "technical-mock-drills": ("interview", "cicd", "kubernetes", "questions_cicd", "questions_k8s"),
    "final-checklist-interview-day": ("master", "interview"),
    "sprint-complete-resources": ("master", "aws", "interview", "career_master"),
    # --- Sweden ---
    "se-devops-battle-plan": ("visa_sweden", "interview", "employers_sweden"),
    "se-visa-sponsor-landscape": ("visa_sweden",),
    "se-employers-and-stacks": ("employers_sweden", "azure"),
    "se-foundations-interview": ("linux", "git", "networking"),
    "se-azure-k8s-stack": ("azure", "kubernetes"),
    "se-cicd-pipeline-interview": ("cicd", "azure", "questions_cicd"),
    "se-terraform-iac": ("terraform", "azure"),
    "se-observability-incidents": ("observability", "questions_sre"),
    "se-security-compliance": ("security",),
    "se-behavioral-culture": ("interview", "questions_behavioral"),
    "se-relocation-practical": ("visa_sweden",),
    "se-mock-drills-final": ("interview", "azure", "kubernetes", "master"),
    "se-complete-resources": ("master", "visa_sweden", "employers_sweden", "azure"),
    # --- Australia ---
    "au-devops-battle-plan": ("visa_australia", "interview", "employers_australia"),
    "au-visa-sponsor-landscape": ("visa_australia",),
    "au-employers-and-stacks": ("employers_australia", "aws"),
    "au-foundations-interview": ("linux", "git", "networking"),
    "au-aws-eks-stack": ("aws", "kubernetes"),
    "au-cicd-compliance": ("cicd", "compliance_au", "questions_cicd"),
    "au-terraform-iac": ("terraform", "aws"),
    "au-observability-incidents": ("observability", "questions_sre"),
    "au-security-devsecops": ("security", "compliance_au"),
    "au-behavioral-culture": ("interview", "questions_behavioral"),
    "au-relocation-practical": ("visa_australia",),
    "au-mock-drills-final": ("interview", "aws", "master"),
    "au-complete-resources": ("master", "visa_australia", "employers_australia", "aws", "compliance_au"),
    # --- New Zealand ---
    "nz-devops-battle-plan": ("visa_nz", "interview", "employers_nz"),
    "nz-visa-sponsor-landscape": ("visa_nz",),
    "nz-employers-and-stacks": ("employers_nz", "aws", "azure"),
    "nz-foundations-interview": ("linux", "git", "docker"),
    "nz-cloud-cicd": ("cicd", "aws", "azure"),
    "nz-kubernetes-iac": ("kubernetes", "terraform"),
    "nz-observability-incidents": ("observability",),
    "nz-security-basics": ("security",),
    "nz-behavioral-culture": ("interview", "questions_behavioral"),
    "nz-relocation-practical": ("visa_nz",),
    "nz-mock-drills-final": ("interview", "master"),
    "nz-complete-resources": ("master", "visa_nz", "employers_nz"),
    # --- USA ---
    "us-devops-battle-plan": ("visa_usa", "interview", "employers_usa"),
    "us-visa-sponsor-landscape": ("visa_usa", "employers_usa"),
    "us-employers-and-stacks": ("employers_usa", "aws"),
    "us-foundations-interview": ("linux", "git", "networking"),
    "us-aws-eks-deep": ("aws", "kubernetes", "questions_k8s"),
    "us-cicd-at-scale": ("cicd", "questions_cicd"),
    "us-terraform-iac": ("terraform", "aws"),
    "us-sre-observability": ("observability", "questions_sre"),
    "us-security-compliance": ("security", "compliance_us"),
    "us-behavioral-negotiation": ("interview", "questions_behavioral", "employers_usa"),
    "us-system-design-infra": ("interview", "aws", "kubernetes"),
    "us-mock-drills-final": ("interview", "master", "aws"),
    "us-complete-resources": ("master", "visa_usa", "employers_usa", "aws", "compliance_us"),
    # --- UK ---
    "uk-devops-battle-plan": ("visa_uk", "interview", "employers_uk"),
    "uk-visa-sponsor-landscape": ("visa_uk", "employers_uk"),
    "uk-employers-and-stacks": ("employers_uk", "aws", "gcp"),
    "uk-foundations-interview": ("linux", "git", "networking"),
    "uk-kubernetes-gitops": ("kubernetes", "cicd"),
    "uk-aws-gcp-cloud": ("aws", "gcp"),
    "uk-cicd-regulated": ("cicd", "compliance_uk", "questions_cicd"),
    "uk-terraform-iac": ("terraform", "aws"),
    "uk-observability-incidents": ("observability", "questions_sre"),
    "uk-security-gdpr": ("security", "compliance_uk"),
    "uk-behavioral-culture": ("interview", "questions_behavioral"),
    "uk-relocation-practical": ("visa_uk",),
    "uk-mock-drills-final": ("interview", "master"),
    "uk-complete-resources": ("master", "visa_uk", "employers_uk", "compliance_uk"),
    # --- DevOps & SRE core roadmap ---
    "cicd-pipeline": ("cicd", "questions_cicd"),
    "containers-runtime": ("docker", "kubernetes"),
    "linux-and-networking-ops": ("linux", "networking"),
    "iac-and-environments": ("terraform", "security"),
    "observability-sre": ("observability", "questions_sre"),
    "incidents": ("observability", "interview"),
    "devops-sre-complete-resources": ("master", "cicd", "kubernetes", "observability"),
}

_CAREER_ROLE_REFS: dict[str, tuple[str, str]] = {
    "de": ("data_engineering", "questions_data"),
    "ds": ("data_science", "questions_data_science"),
    "dso": ("devsecops", "questions_devsecops"),
    "df": ("data_shared", "questions_data"),
    "qa": ("qa_sdet", "questions_qa"),
    "be": ("backend_role", "questions_backend"),
    "ce": ("cloud_role", "questions_cloud"),
}

_CAREER_REGION_REFS: dict[str, tuple[str, str]] = {
    "se": ("visa_sweden", "employers_sweden"),
    "au": ("visa_australia", "employers_australia"),
    "nz": ("visa_nz", "employers_nz"),
    "us": ("visa_usa", "employers_usa"),
    "uk": ("visa_uk", "employers_uk"),
}

_SPONSOR_REGION_REFS: dict[str, tuple[str, ...]] = {
    "se": ("visa_sweden", "employers_sweden", "employer_volvo", "employer_ifs", "questions_enterprise"),
    "au": ("visa_australia", "employers_australia", "employer_ifs", "compliance_au"),
    "us": ("visa_usa", "employers_usa", "employer_ifs", "employer_volvo", "compliance_us"),
}


def _dedupe_keys(keys: list[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    return tuple(k for k in keys if not (k in seen or seen.add(k)))


def _sponsor_ref_keys(slug: str) -> tuple[str, ...] | None:
    if not slug.startswith("sp-"):
        return None
    parts = slug.split("-")
    if len(parts) < 3:
        return None
    code = parts[1]
    region_refs = _SPONSOR_REGION_REFS.get(code)
    if region_refs is None:
        return None
    keys: list[str] = ["interview", "career_master", *region_refs]
    tail = "-".join(parts[2:])
    if "volvo" in tail:
        keys.append("employer_volvo")
    if "ifs" in tail:
        keys.append("employer_ifs")
    if tail.endswith("interviews") or tail.endswith("tier1"):
        keys.extend(["questions_cicd", "questions_k8s", "questions_enterprise"])
    if tail.endswith("banks") or "regulated" in tail:
        keys.append("compliance_au")
    if tail == "checklist" or tail == "intro":
        keys.append("career_master")
    return _dedupe_keys(keys)


def _relocation_ref_keys(slug: str) -> tuple[str, ...] | None:
    if not slug.startswith("reloc-"):
        return None
    parts = slug.split("-")
    if len(parts) < 3:
        return None
    code = parts[1]
    region_refs = _CAREER_REGION_REFS.get(code)
    if region_refs is None:
        return None
    keys: list[str] = ["interview", "career_master", region_refs[0]]
    tail = "-".join(parts[2:])
    if tail == "employers":
        keys.append(region_refs[1])
    if tail == "culture":
        keys.append("questions_behavioral")
    if tail == "checklist":
        keys.append(region_refs[1])
    return _dedupe_keys(keys)


def _career_ref_keys(slug: str) -> tuple[str, ...] | None:
    """Resolve reference keys for generated career path lessons (de-, ds-, dso-, df-, etc.)."""
    sponsor = _sponsor_ref_keys(slug)
    if sponsor:
        return sponsor
    reloc = _relocation_ref_keys(slug)
    if reloc:
        return reloc

    for short, (role_ref, questions_ref) in _CAREER_ROLE_REFS.items():
        prefix = f"{short}-"
        if not slug.startswith(prefix):
            continue
        tail = slug[len(prefix) :]
        keys: list[str] = ["interview", role_ref]
        region_refs: tuple[str, str] | None = None
        for rp, refs in _CAREER_REGION_REFS.items():
            region_prefix = f"{rp}-"
            if tail.startswith(region_prefix):
                region_refs = refs
                tail = tail[len(region_prefix) :]
                keys.extend(refs)
                break

        if "battle-plan" in slug or "complete-resources" in slug or slug.endswith("-checklist"):
            keys.append("career_master")
        if tail == "visa-landscape" and region_refs:
            keys.append(region_refs[0])
        if tail == "employers-stacks" and region_refs:
            keys.append(region_refs[1])
        if tail == "foundations" or tail.startswith("core"):
            if short == "de":
                keys.append("terraform")
            if short == "be":
                keys.append("backend_role")
            if short == "dso":
                keys.extend(["security", "cicd"])
            if short in ("de", "ds", "df"):
                keys.append("data_shared")
        if tail.startswith("core") or tail == "mock-final" or tail == "week1-checkpoint":
            keys.append(questions_ref)
        if tail == "behavioral":
            keys.append("questions_behavioral")
        if short == "ce" and tail.startswith("core"):
            keys.extend(["terraform", "aws", "azure"])
        if short == "qa" and "core2" in tail:
            keys.append("cicd")
        if short == "df":
            keys.append("data_shared")
            if slug.endswith("-intro") or slug.endswith("-checklist"):
                keys.append("career_master")

        return _dedupe_keys(keys)
    return None


def ref_keys_for_lesson(slug: str, inline: tuple[str, ...] | None = None) -> tuple[str, ...]:
    if inline:
        return inline
    if slug in LESSON_REF_KEYS:
        return LESSON_REF_KEYS[slug]
    career = _career_ref_keys(slug)
    if career:
        return career
    return ("interview",)
