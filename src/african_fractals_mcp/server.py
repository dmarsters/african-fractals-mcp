#!/usr/bin/env python3
"""
African Fractals MCP Server

Based on Ron Eglash's ethnomathematical research documenting intentional
mathematical knowledge encoded in African design traditions.

Three-layer architecture:
- Layer 1: YAML olog taxonomy lookup (zero LLM cost)
- Layer 2: Deterministic parameter mapping (zero LLM cost)  
- Layer 3: Claude synthesis of final prompt (LLM synthesis)
"""

from fastmcp import FastMCP
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
import yaml
import re
import numpy as np
import math

# Initialize server
mcp = FastMCP("african-fractals")

# Load olog specification
_olog_path = Path(__file__).parent / "ologs" / "african_fractals.olog.yaml"
with open(_olog_path) as f:
    OLOG = yaml.safe_load(f)

# Extract taxonomy sections for quick access
TRADITIONS = OLOG["types"]["tradition"]["values"]
RECURSION_TYPES = OLOG["types"]["recursion_type"]["values"]
SYMMETRY_MODES = OLOG["types"]["symmetry_mode"]["values"]
SCALE_RELATIONSHIPS = OLOG["types"]["scale_relationship"]["values"]
INTENT_MAPPINGS = OLOG["morphisms"]["intent_to_tradition"]["mappings"]
INTENTIONALITY = OLOG["intentionality"]


# =============================================================================
# LAYER 1: Pure Taxonomy Lookup (Zero LLM Cost)
# =============================================================================

@mcp.tool()
def list_traditions() -> Dict[str, Any]:
    """
    List all available African fractal traditions with their regions and primary forms.
    
    Returns:
        Formatted list of traditions with cultural attribution
    """
    result = ["# African Fractal Traditions\n"]
    result.append("Each tradition represents a distinct mathematical knowledge system.\n")
    
    for name, data in TRADITIONS.items():
        result.append(f"\n## {name.replace('_', ' ').title()}")
        result.append(f"- **Culture**: {data['culture']}")
        result.append(f"- **Region**: {data['region']}")
        result.append(f"- **Primary Form**: {data['primary_form']}")
        result.append(f"- **Recursion Type**: {data['recursion_type']}")
    
    return {"content": "\n".join(result)}


@mcp.tool()
def get_tradition_profile(tradition_name: str) -> Dict[str, Any]:
    """
    Get complete profile for a specific tradition including geometry,
    visual parameters, and intentionality.
    
    Args:
        tradition_name: Name of tradition (e.g., "ba_ila_settlements", "dogon_architecture")
    
    Returns:
        Complete tradition profile as formatted text
    """
    # Normalize name
    key = tradition_name.lower().replace(" ", "_").replace("-", "_")
    
    if key not in TRADITIONS:
        available = ", ".join(TRADITIONS.keys())
        return {"content": f"Tradition '{tradition_name}' not found. Available: {available}"}
    
    tradition = TRADITIONS[key]
    
    result = [f"# {tradition_name.replace('_', ' ').title()}\n"]
    result.append(f"**Culture**: {tradition['culture']}")
    result.append(f"**Region**: {tradition['region']}")
    result.append(f"**Primary Form**: {tradition['primary_form']}")
    result.append(f"**Recursion Type**: {tradition['recursion_type']}\n")
    
    # Geometry
    if "geometry" in tradition:
        result.append("## Geometry")
        for k, v in tradition["geometry"].items():
            result.append(f"- **{k.replace('_', ' ').title()}**: {v}")
    
    # Visual parameters
    if "visual_parameters" in tradition:
        result.append("\n## Visual Parameters")
        for k, v in tradition["visual_parameters"].items():
            result.append(f"- **{k.replace('_', ' ').title()}**: {v}")
    
    # Intentionality
    if "intentionality" in tradition:
        result.append("\n## Intentionality (Why This Pattern)")
        for k, v in tradition["intentionality"].items():
            result.append(f"- **{k.replace('_', ' ').title()}**: {v}")
    
    # Color associations
    if "color_associations" in tradition:
        result.append("\n## Color Associations")
        for k, v in tradition["color_associations"].items():
            if isinstance(v, list):
                result.append(f"- **{k.replace('_', ' ').title()}**: {', '.join(v)}")
            else:
                result.append(f"- **{k.replace('_', ' ').title()}**: {v}")
    
    return {"content": "\n".join(result)}


@mcp.tool()
def list_recursion_types() -> Dict[str, Any]:
    """
    List all recursion types with their visual signatures and mathematical properties.
    
    Returns:
        Formatted list of recursion mechanisms
    """
    result = ["# Recursion Types in African Fractal Design\n"]
    
    for name, data in RECURSION_TYPES.items():
        result.append(f"\n## {name.replace('_', ' ').title()}")
        result.append(f"**Description**: {data['description']}")
        result.append(f"**Visual Signature**: {data['visual_signature']}")
        result.append(f"**Mathematical Property**: {data['mathematical_property']}")
        result.append(f"**Example Traditions**: {', '.join(data['example_traditions'])}")
    
    return {"content": "\n".join(result)}


@mcp.tool()
def list_symmetry_modes() -> Dict[str, Any]:
    """
    List symmetry modes showing how recursion interacts with symmetry operations.
    
    Returns:
        Formatted list of symmetry modes
    """
    result = ["# Symmetry Modes\n"]
    
    for name, data in SYMMETRY_MODES.items():
        result.append(f"\n## {name.replace('_', ' ').title()}")
        result.append(f"**Description**: {data['description']}")
        result.append(f"**Visual Signature**: {data['visual_signature']}")
        result.append(f"**Traditions**: {', '.join(data['traditions'])}")
        if "intentionality" in data:
            result.append(f"**Intentionality**: {data['intentionality']}")
    
    return {"content": "\n".join(result)}


@mcp.tool()
def get_intentionality_principles() -> Dict[str, Any]:
    """
    Get the core intentionality principles explaining why African fractal patterns work.
    
    Returns:
        Formatted intentionality documentation
    """
    result = ["# Intentionality Principles\n"]
    result.append(f"**Core Principle**: {INTENTIONALITY['core_principle']}\n")
    
    for category, data in INTENTIONALITY.items():
        if category == "core_principle":
            continue
        
        result.append(f"\n## {category.replace('_', ' ').title()}")
        
        if isinstance(data, dict):
            if "description" in data:
                result.append(f"{data['description']}\n")
            
            if "examples" in data:
                result.append("**Examples**:")
                for ex in data["examples"]:
                    if isinstance(ex, dict):
                        result.append(f"- {ex.get('tradition', 'N/A')}: {ex.get('encoding', ex.get('constraint', 'N/A'))}")
                    else:
                        result.append(f"- {ex}")
            
            if "visual_implication" in data:
                result.append(f"\n**Visual Implication**: {data['visual_implication']}")
    
    return {"content": "\n".join(result)}


# =============================================================================
# LAYER 2: Deterministic Parameter Mapping (Zero LLM Cost)
# =============================================================================

@mcp.tool()
def map_intent_to_tradition(
    intent: str
) -> Dict[str, Any]:
    """
    Map creative intent to recommended tradition and parameters.
    
    LAYER 2 - Deterministic mapping, zero LLM cost.
    
    Args:
        intent: Creative intent keyword. Options:
            - "contained_complexity": Bounded complexity
            - "organic_growth": Living, branching expansion
            - "sacred_elaboration": Spiritual infinite detail
            - "encoded_knowledge": Information in pattern
            - "social_hierarchy": Power and status in scale
            - "textile_rhythm": Woven rhythmic patterns
    
    Returns:
        Recommended tradition and parameters
    """
    key = intent.lower().replace(" ", "_").replace("-", "_")
    
    if key not in INTENT_MAPPINGS:
        available = ", ".join(INTENT_MAPPINGS.keys())
        return {"content": f"Intent '{intent}' not found. Available: {available}"}
    
    mapping = INTENT_MAPPINGS[key]
    
    result = [f"# Intent Mapping: {intent}\n"]
    result.append(f"**Description**: {mapping['description']}")
    result.append(f"**Primary Traditions**: {', '.join(mapping['primary_traditions'])}")
    result.append(f"**Secondary Traditions**: {', '.join(mapping['secondary_traditions'])}")
    result.append(f"**Recursion Type**: {mapping['recursion_type']}")
    result.append(f"**Visual Result**: {mapping['visual_result']}")
    
    # Get first primary tradition's full profile
    primary = mapping['primary_traditions'][0]
    if primary in TRADITIONS:
        result.append(f"\n## Recommended: {primary.replace('_', ' ').title()}")
        tradition = TRADITIONS[primary]
        result.append(f"- Culture: {tradition['culture']}")
        result.append(f"- Region: {tradition['region']}")
        if "geometry" in tradition:
            result.append(f"- Base Shape: {tradition['geometry'].get('base_shape', 'N/A')}")
            result.append(f"- Scale Ratio: {tradition['geometry'].get('scale_ratio', 'N/A')}")
            result.append(f"- Typical Depth: {tradition['geometry'].get('typical_depth', 'N/A')}")
    
    return {"content": "\n".join(result)}


@mcp.tool()
def build_visual_parameters(
    tradition_name: str,
    recursion_depth: int = 3,
    symmetry_mode: Optional[str] = None,
    scale_ratio: Optional[str] = None,
    include_imperfection: bool = True
) -> Dict[str, Any]:
    """
    Build complete visual parameters from tradition and options.
    
    LAYER 2 - Deterministic assembly, zero LLM cost.
    
    Args:
        tradition_name: Specific tradition (e.g., "ba_ila_settlements")
        recursion_depth: Number of recursive levels (1-5)
        symmetry_mode: Override symmetry (or use tradition default)
        scale_ratio: Override scale ratio (or use tradition default)
        include_imperfection: Whether to include deliberate irregularity (recommended)
    
    Returns:
        Complete parameter dictionary ready for synthesis
    """
    key = tradition_name.lower().replace(" ", "_").replace("-", "_")
    
    if key not in TRADITIONS:
        return {"error": f"Tradition '{tradition_name}' not found"}
    
    tradition = TRADITIONS[key]
    
    # Build parameters
    params = {
        "tradition": {
            "name": key,
            "display_name": tradition_name.replace("_", " ").title(),
            "culture": tradition["culture"],
            "region": tradition["region"],
            "primary_form": tradition["primary_form"]
        },
        "recursion": {
            "type": tradition["recursion_type"],
            "depth": min(max(recursion_depth, 1), 5),
            "depth_description": _describe_depth(recursion_depth)
        },
        "geometry": tradition.get("geometry", {}),
        "visual_parameters": tradition.get("visual_parameters", {}),
        "color_palette": tradition.get("color_associations", {}),
        "intentionality": tradition.get("intentionality", {}),
        "deliberate_imperfection": include_imperfection
    }
    
    # Override symmetry if provided
    if symmetry_mode:
        params["symmetry_override"] = symmetry_mode
    else:
        # Infer from visual parameters
        params["symmetry"] = tradition.get("visual_parameters", {}).get(
            "symmetry", "bilateral_recursive"
        )
    
    # Override scale ratio if provided
    if scale_ratio:
        params["geometry"]["scale_ratio"] = scale_ratio
    
    # Add imperfection guidance
    if include_imperfection:
        params["imperfection_guidance"] = {
            "principle": "Deliberate irregularity authenticates human origin",
            "techniques": [
                "Subtle asymmetry in bilateral forms",
                "Slight spacing variation in repetitions",
                "Minor edge wobble rather than perfect lines",
                "Small proportion shifts between recursion levels"
            ]
        }
    
    return params


def _describe_depth(depth: int) -> str:
    """Human-readable description of recursion depth."""
    descriptions = {
        1: "Minimal - suggests recursion without showing it",
        2: "Shallow - clear parent-child relationship",
        3: "Moderate - clear fractal nature, readable structure",
        4: "Deep - rich complexity, rewards close attention",
        5: "Very deep - dense detail, texture-like at distance"
    }
    return descriptions.get(depth, "Unknown")


# =============================================================================
# LAYER 3: Synthesis Support (Prepares Context for Claude)
# =============================================================================

@mcp.tool()
def enhance_with_african_fractals(
    base_prompt: str,
    tradition_name: str,
    intent: Optional[str] = None,
    recursion_depth: int = 3,
    include_imperfection: bool = True,
    include_educational_gateway: bool = True
) -> Dict[str, Any]:
    """
    Enhance an image generation prompt with African fractal aesthetics.
    
    This tool provides structured parameters for Claude to synthesize
    into a coherent enhanced prompt. It ensures cultural attribution
    and mathematical coherence.
    
    By default, includes links to CSDT interactive tools so users can
    explore the actual mathematics, positioning this brick as a gateway
    to deeper engagement rather than a substitute for it.
    
    Args:
        base_prompt: Original image concept
        tradition_name: Specific tradition to draw from
        intent: Optional creative intent for additional guidance
        recursion_depth: Recursive levels (1-5)
        include_imperfection: Include deliberate irregularity
        include_educational_gateway: Include CSDT resource links (recommended)
    
    Returns:
        Complete enhancement data for synthesis including educational resources
    """
    # Get visual parameters
    params = build_visual_parameters(
        tradition_name=tradition_name,
        recursion_depth=recursion_depth,
        include_imperfection=include_imperfection
    )
    
    if "error" in params:
        return params
    
    # Add intent mapping if provided
    if intent:
        intent_key = intent.lower().replace(" ", "_")
        if intent_key in INTENT_MAPPINGS:
            params["intent_guidance"] = INTENT_MAPPINGS[intent_key]
    
    # Build synthesis context
    result = {
        "base_prompt": base_prompt,
        "tradition_parameters": params,
        "cultural_attribution": {
            "required": True,
            "culture": params["tradition"]["culture"],
            "region": params["tradition"]["region"],
            "note": "Always attribute specific cultural source, never generic 'African'"
        },
        "synthesis_instruction": _build_synthesis_instruction(params),
        "negative_guidance": [
            "Avoid generic 'tribal' or 'ethnic' descriptors",
            "Do not mix elements from different traditions",
            "Avoid machine-perfect regularity",
            "Do not imply primitiveness or accident"
        ]
    }
    
    # Add educational gateway
    if include_educational_gateway:
        key = tradition_name.lower().replace(" ", "_").replace("-", "_")
        
        result["educational_gateway"] = {
            "philosophy": "This brick is a gateway to deeper engagement, not a substitute",
            "primary_resources": {
                "csdt_main": "https://csdt.org/",
                "african_fractals_hub": "https://csdt.org/culture/africanfractals/index.html",
                "ted_talk": "https://www.ted.com/talks/ron_eglash_the_fractals_at_the_heart_of_african_designs"
            },
            "suggestion_for_response": f"""
Consider including in your response:
"To explore the mathematics of {params['tradition']['display_name']} interactively, 
visit the Culturally Situated Design Tools: https://csdt.org/culture/africanfractals/index.html"
"""
        }
        
        # Add tradition-specific CSDT resources if available
        if key in CSDT_RESOURCES:
            result["educational_gateway"]["tradition_specific"] = CSDT_RESOURCES[key]
    
    return result


def _build_synthesis_instruction(params: Dict[str, Any]) -> str:
    """Build instruction for Claude's synthesis layer."""
    tradition = params["tradition"]
    recursion = params["recursion"]
    
    instruction = f"""
Synthesize an enhanced prompt incorporating {tradition['display_name']} fractal aesthetics.

Key requirements:
1. Cultural attribution: {tradition['culture']} tradition from {tradition['region']}
2. Recursion: {recursion['type']} pattern at {recursion['depth']} levels ({recursion['depth_description']})
3. Material: Reference tradition's actual medium - {params.get('visual_parameters', {}).get('material_contexts', tradition['primary_form'])}
4. Color: Draw from {list(params.get('color_palette', {}).keys())} palette
5. Imperfection: {'Include deliberate irregularity' if params.get('deliberate_imperfection') else 'May use regular precision'}

The pattern should encode intentional meaning, not decorative accident.
Mathematical relationships should be coherent within tradition's rules.
"""
    return instruction.strip()


@mcp.tool()
def get_composition_guidance(other_domain: str) -> Dict[str, Any]:
    """
    Get guidance for composing African fractals with another Lushy domain.
    
    Args:
        other_domain: Name of other brick (e.g., "origami", "jazz", "genetic")
    
    Returns:
        Composition guidance and mapping suggestions
    """
    compositions = OLOG.get("composition", {}).get("compatible_domains", {})
    
    key = other_domain.lower().replace(" ", "_").replace("-", "_")
    
    # Try to find matching domain
    matching_key = None
    for k in compositions.keys():
        if key in k or k in key:
            matching_key = k
            break
    
    if not matching_key:
        available = ", ".join(compositions.keys())
        return {"content": f"Domain '{other_domain}' not found. Available compositions: {available}"}
    
    comp = compositions[matching_key]
    
    result = [f"# Composing with {matching_key.replace('_', ' ').title()}\n"]
    result.append(f"**Connection**: {comp['connection']}\n")
    
    result.append("## Mappings")
    for source, target in comp["mapping"].items():
        result.append(f"- {source} → {target}")
    
    result.append(f"\n**Composition Strategy**: {comp['composition_strategy']}")
    
    # Add conflict resolution
    conflict = OLOG.get("composition", {}).get("conflict_resolution", {})
    if conflict:
        result.append("\n## Conflict Resolution")
        result.append(f"**Principle**: {conflict.get('principle', 'N/A')}")
        if "strategy" in conflict:
            result.append("\n**Strategy**:")
            for s in conflict["strategy"]:
                result.append(f"- {s}")
    
    return {"content": "\n".join(result)}


@mcp.tool()
def get_example_compositions() -> Dict[str, Any]:
    """
    Get example compositions showing full parameter sets and prompt sketches.
    
    Returns:
        Formatted examples from the olog
    """
    examples = OLOG.get("examples", [])
    
    if not examples:
        return {"content": "No examples found in olog."}
    
    result = ["# Example Compositions\n"]
    
    for ex in examples:
        result.append(f"\n## {ex['name']}")
        result.append(f"**Tradition**: {ex['tradition']}")
        result.append(f"**Intent**: {ex['intent']}")
        
        result.append("\n### Parameters")
        for k, v in ex["parameters"].items():
            result.append(f"- **{k}**: {v}")
        
        result.append(f"\n### Prompt Sketch\n{ex['prompt_sketch']}")
    
    return {"content": "\n".join(result)}


# =============================================================================
# EDUCATIONAL RESOURCES: Gateway to Deeper Engagement
# =============================================================================

# CSDT resource mapping - verified URLs for interactive simulations
CSDT_RESOURCES = {
    "ba_ila_settlements": {
        "csdt_hub": "https://csdt.org/culture/africanfractals/index.html",
        "section": "African Architecture",
        "mathematical_concepts": ["scaling iteration", "nested circles", "geometric transformation"],
        "interactive_parameters": [
            "ring_count: Number of concentric settlement rings",
            "scale_factor: Size ratio between parent and child rings",
            "rotation: Angular offset between levels",
            "opening_angle: Gap width for pathways"
        ]
    },
    "dogon_architecture": {
        "csdt_hub": "https://csdt.org/culture/africanfractals/index.html",
        "section": "African Architecture", 
        "mathematical_concepts": ["rectangular nesting", "anthropomorphic mapping", "modular design"],
        "interactive_parameters": [
            "nesting_depth: Levels of room-within-room",
            "proportion_ratio: Width to height relationships",
            "module_placement: Anthropomorphic position mapping"
        ]
    },
    "fulani_wedding_blankets": {
        "csdt_hub": "https://csdt.org/culture/africanfractals/index.html",
        "section": "African Art",
        "mathematical_concepts": ["self-affine scaling", "bilateral symmetry", "iterative pattern"],
        "interactive_parameters": [
            "motif_scale: Size of repeated elements",
            "iteration_depth: Levels of nested motifs",
            "band_rhythm: Spacing between horizontal bands"
        ]
    },
    "ethiopian_processional_crosses": {
        "csdt_hub": "https://csdt.org/culture/africanfractals/index.html",
        "section": "African Religion",
        "mathematical_concepts": ["edge elaboration", "iterative complexity", "rotational symmetry"],
        "interactive_parameters": [
            "elaboration_depth: Iterations of edge replacement",
            "cross_type: Base cross form (Greek, Latin, etc.)",
            "lattice_density: Interior piercing complexity"
        ]
    },
    "akan_goldweights": {
        "csdt_hub": "https://csdt.org/culture/africanfractals/index.html",
        "section": "African Art",
        "mathematical_concepts": ["self-similarity", "proportional scaling", "symbolic encoding"],
        "interactive_parameters": [
            "form_type: Geometric vs figurative base",
            "scale_ratio: Size relationship in self-similar elements"
        ]
    },
    "mangbetu_design": {
        "csdt_hub": "https://csdt.org/culture/africanfractals/index.html",
        "related_csdt": "Mangbetu Design tool available in CSDT suite",
        "mathematical_concepts": ["self-affine transformation", "elongation scaling", "surface tessellation"],
        "interactive_parameters": [
            "elongation_factor: Vertical stretch ratio",
            "pattern_density: Surface coverage intensity",
            "iteration_count: Nested pattern levels"
        ]
    },
    "cornrow_hairstyles": {
        "csdt_tool": "https://csdt.org/projects?search=cornrow",
        "tool_name": "Cornrow Curves",
        "mathematical_concepts": ["transformational geometry", "iteration", "logarithmic spirals"],
        "note": "First CSDT tool developed, focused on connecting popular culture to mathematics",
        "interactive_parameters": [
            "curve_type: Spiral form (logarithmic, Archimedean)",
            "iteration_count: Braid complexity",
            "rotation_angle: Curve direction changes",
            "scale_factor: Size change per iteration"
        ]
    },
    "bamana_divination": {
        "csdt_hub": "https://csdt.org/culture/africanfractals/index.html",
        "section": "African Religion",
        "mathematical_concepts": ["binary recursion", "algorithmic generation", "decision trees"],
        "interactive_parameters": [
            "generation_depth: Binary tree iterations",
            "randomization: Input entropy level",
            "grid_size: Base layout dimensions"
        ]
    }
}


@mcp.tool()
def get_educational_resources(tradition_name: str) -> Dict[str, Any]:
    """
    Get links to primary educational resources for deeper engagement.
    
    Returns CSDT interactive tools, mathematical concepts, and parameters
    that let users explore the actual mathematics, not just the aesthetics.
    
    Philosophy: This brick should be a GATEWAY to the living educational 
    project, not a substitute for it. Generated images are downstream of 
    knowledge systems users can engage with directly.
    
    Args:
        tradition_name: Name of tradition (e.g., "ba_ila_settlements")
    
    Returns:
        Educational resource links and interactive parameter descriptions
    """
    key = tradition_name.lower().replace(" ", "_").replace("-", "_")
    
    # Base resources available for all
    base_resources = {
        "csdt_main_site": "https://csdt.org/",
        "african_fractals_hub": "https://csdt.org/culture/africanfractals/index.html",
        "ted_talk": "https://www.ted.com/talks/ron_eglash_the_fractals_at_the_heart_of_african_designs",
        "primary_source": {
            "title": "African Fractals: Modern Computing and Indigenous Design",
            "author": "Ron Eglash",
            "year": 1999,
            "publisher": "Rutgers University Press"
        }
    }
    
    if key in CSDT_RESOURCES:
        tradition_resources = CSDT_RESOURCES[key]
        return {
            "tradition": key,
            "csdt_resources": tradition_resources,
            "general_resources": base_resources,
            "engagement_suggestion": f"""
To explore the mathematics interactively:
1. Visit {tradition_resources.get('csdt_hub', tradition_resources.get('csdt_tool', base_resources['african_fractals_hub']))}
2. Navigate to the {tradition_resources.get('section', 'relevant')} section
3. Try manipulating: {', '.join(tradition_resources['interactive_parameters'][:2])}

The CSDT tools let you SEE how parameter changes affect the pattern,
building intuition for the mathematical relationships encoded in {key.replace('_', ' ')}.
""",
            "bidirectional_value": """
CSDT creates bidirectional value:
- You learn mathematics through cultural heritage
- Cultural knowledge gains visibility through math education

Your generated images are downstream of living knowledge systems 
you can engage with directly through these tools.
"""
        }
    else:
        return {
            "tradition": key,
            "note": f"Specific CSDT tool not mapped for {key}, but general resources available",
            "general_resources": base_resources,
            "engagement_suggestion": f"""
While a specific CSDT simulation for {key.replace('_', ' ')} may not be mapped,
you can explore related African fractal mathematics at:
{base_resources['african_fractals_hub']}

The general principles of recursion, scaling, and self-similarity
apply across traditions.
"""
        }


@mcp.tool()
def get_all_csdt_resources() -> Dict[str, Any]:
    """
    Get overview of all CSDT educational resources mapped to traditions.
    
    Returns:
        Formatted summary of available interactive tools and their mathematical focus
    """
    result = ["# CSDT Educational Resources\n"]
    result.append("Interactive tools for exploring the mathematics of African fractal design.\n")
    result.append("**Main Site**: https://csdt.org/")
    result.append("**African Fractals Hub**: https://csdt.org/culture/africanfractals/index.html\n")
    
    result.append("## Available Tool Mappings\n")
    
    for tradition, resources in CSDT_RESOURCES.items():
        result.append(f"### {tradition.replace('_', ' ').title()}")
        if "csdt_tool" in resources:
            result.append(f"**Direct Tool**: {resources['csdt_tool']}")
        elif "csdt_hub" in resources:
            result.append(f"**Hub Section**: {resources.get('section', 'General')}")
        
        result.append(f"**Mathematical Concepts**: {', '.join(resources['mathematical_concepts'])}")
        result.append("**Interactive Parameters**:")
        for param in resources['interactive_parameters'][:3]:  # Show top 3
            result.append(f"  - {param}")
        result.append("")
    
    result.append("## Pedagogical Philosophy")
    result.append("""
The CSDT project demonstrates that African fractal designs encode intentional
mathematical knowledge. The interactive tools let users:

1. **Manipulate parameters** and see immediate visual results
2. **Build intuition** for scaling ratios, recursion depth, symmetry
3. **Connect heritage to STEM** - cultural patterns teach mathematical concepts
4. **Create original designs** using the same algorithms as traditional artisans

This brick should function as a gateway to these tools, not a replacement.
""")
    
    return {"content": "\n".join(result)}


# =============================================================================
# TOMOGRAPHIC STRATEGY ANALYSIS
# =============================================================================

# Strategic pattern definitions for African Fractals domain
STRATEGIC_PATTERNS = {
    "recursive_structure": {
        "nested_goals": {
            "pattern": r"(?:goal|objective|principle|value).*?(?:contain|include|comprise|nest|embed|subsume)",
            "threshold": 3,
            "confidence": 0.75,
        },
        "self_similar_language": {
            "pattern": r"(?:at (?:each|every|all) (?:level|scale|tier))|(?:across (?:all )?(?:level|scale|tier)s?)|(?:same .{1,20} (?:repeated|replicated|echoed))",
            "threshold": 2,
            "confidence": 0.80,
        },
        "iteration_markers": {
            "pattern": r"(?:iteration|recursive|nested|layered|multi-level|hierarchical structure|fractal)",
            "threshold": 3,
            "confidence": 0.70,
        },
    },
    "scaling_relationship": {
        "self_similar": {
            "pattern": r"(?:uniform|consistent|identical|same proportion|equal ratio|constant scale)",
            "threshold": 2,
            "confidence": 0.75,
        },
        "self_affine": {
            "pattern": r"(?:different proportion|varying ratio|scaled differently|disproportionate|asymmetric scaling|elongat)",
            "threshold": 2,
            "confidence": 0.75,
        },
        "proportional_language": {
            "pattern": r"(?:ratio|proportion|scale factor|scaling|relative size)",
            "threshold": 2,
            "confidence": 0.65,
        },
    },
    "intentionality": {
        "purpose_before_form": {
            "pattern": r"(?:(?:in order to|to achieve|for the purpose of|intended to|designed to).{1,40}(?:then|therefore|thus|subsequently))",
            "threshold": 2,
            "confidence": 0.80,
        },
        "knowledge_encoding": {
            "pattern": r"(?:embed|encode|contain|preserve|transmit|store).{1,30}(?:knowledge|wisdom|understanding|information|principle)",
            "threshold": 2,
            "confidence": 0.75,
        },
        "functional_constraint": {
            "pattern": r"(?:constraint|requirement|must|necessary|essential).{1,40}(?:inform|shape|determine|drive).{1,30}(?:design|structure|form|pattern)",
            "threshold": 2,
            "confidence": 0.70,
        },
    },
    "symmetry_operations": {
        "rotational": {
            "pattern": r"(?:rotat|radial|circular|angular|around|orbit|revolve)",
            "threshold": 2,
            "confidence": 0.70,
        },
        "bilateral": {
            "pattern": r"(?:bilateral|mirror|symmetric|balanced|reflection|left.{1,20}right)",
            "threshold": 2,
            "confidence": 0.70,
        },
        "spiral": {
            "pattern": r"(?:spiral|helical|logarithmic|outward|expanding|unfolding)",
            "threshold": 2,
            "confidence": 0.75,
        },
    },
    "cultural_attribution": {
        "respectful_sourcing": {
            "pattern": r"(?:based on|derived from|inspired by|acknowledging|honoring|rooted in|following).{1,40}(?:tradition|culture|heritage|practice|knowledge)",
            "threshold": 2,
            "confidence": 0.80,
        },
        "extractive_language": {
            "pattern": r"(?:borrow|take|use|leverage|utilize|apply).{1,30}(?:aesthetic|pattern|style|look)",
            "inverse": True,  # High matches = problematic
            "threshold": 3,
            "confidence": 0.75,
        },
        "attribution_markers": {
            "pattern": r"(?:credit|attribution|acknowledgment|recognition|source|origin)",
            "threshold": 2,
            "confidence": 0.70,
        },
    },
}


def detect_recursive_structure(text: str) -> Tuple[Optional[str], float, List[str]]:
    """Detect fractal/recursive organizational patterns in strategy text."""
    
    nested_goals = len(re.findall(
        STRATEGIC_PATTERNS["recursive_structure"]["nested_goals"]["pattern"],
        text, re.IGNORECASE
    ))
    
    self_similar = len(re.findall(
        STRATEGIC_PATTERNS["recursive_structure"]["self_similar_language"]["pattern"],
        text, re.IGNORECASE
    ))
    
    iterations = len(re.findall(
        STRATEGIC_PATTERNS["recursive_structure"]["iteration_markers"]["pattern"],
        text, re.IGNORECASE
    ))
    
    evidence = []
    
    # Strong nesting with self-similar language = fractal recursion
    if (nested_goals >= STRATEGIC_PATTERNS["recursive_structure"]["nested_goals"]["threshold"] and 
        self_similar >= STRATEGIC_PATTERNS["recursive_structure"]["self_similar_language"]["threshold"]):
        evidence.extend([
            f"Found {nested_goals} nested goal structures",
            f"Found {self_similar} self-similar language patterns",
            "Fractal recursion: same principles at each scale"
        ])
        return "fractal_recursion", 0.85, evidence
    
    # Strong iteration markers = iterative deepening
    if iterations >= STRATEGIC_PATTERNS["recursive_structure"]["iteration_markers"]["threshold"]:
        evidence.extend([
            f"Found {iterations} iteration/recursive markers",
            "Iterative deepening: sequential nesting pattern"
        ])
        return "iterative_deepening", 0.75, evidence
    
    # Moderate nesting without self-similarity = simple hierarchy
    if nested_goals >= 2:
        evidence.append(f"Found {nested_goals} nested structures (simple hierarchy, not fractal)")
        return "simple_hierarchy", 0.65, evidence
    
    return None, 0.0, []


def detect_scaling_relationship(text: str) -> Tuple[Optional[str], float, List[str]]:
    """Detect self-similar vs self-affine scaling patterns."""
    
    self_similar = len(re.findall(
        STRATEGIC_PATTERNS["scaling_relationship"]["self_similar"]["pattern"],
        text, re.IGNORECASE
    ))
    
    self_affine = len(re.findall(
        STRATEGIC_PATTERNS["scaling_relationship"]["self_affine"]["pattern"],
        text, re.IGNORECASE
    ))
    
    proportional = len(re.findall(
        STRATEGIC_PATTERNS["scaling_relationship"]["proportional_language"]["pattern"],
        text, re.IGNORECASE
    ))
    
    evidence = []
    
    # Self-similar: uniform scaling at all levels
    if (self_similar >= STRATEGIC_PATTERNS["scaling_relationship"]["self_similar"]["threshold"] and 
        proportional >= 1):
        evidence.extend([
            f"Found {self_similar} uniform scaling markers",
            f"Found {proportional} proportional relationship references",
            "Self-similar: consistent proportions across scales"
        ])
        return "self_similar", 0.80, evidence
    
    # Self-affine: different scaling in different dimensions
    if (self_affine >= STRATEGIC_PATTERNS["scaling_relationship"]["self_affine"]["threshold"] and 
        proportional >= 1):
        evidence.extend([
            f"Found {self_affine} variable scaling markers",
            f"Found {proportional} proportional relationship references",
            "Self-affine: different proportions in different dimensions"
        ])
        return "self_affine", 0.80, evidence
    
    # Proportional language without clear type
    if proportional >= STRATEGIC_PATTERNS["scaling_relationship"]["proportional_language"]["threshold"]:
        evidence.append(f"Found {proportional} proportional relationships (type unclear)")
        return "proportional_unspecified", 0.65, evidence
    
    return None, 0.0, []


def detect_intentionality(text: str) -> Tuple[Optional[str], float, List[str]]:
    """Detect intentional design vs decorative appropriation."""
    
    purpose_first = len(re.findall(
        STRATEGIC_PATTERNS["intentionality"]["purpose_before_form"]["pattern"],
        text, re.IGNORECASE
    ))
    
    knowledge_encoding = len(re.findall(
        STRATEGIC_PATTERNS["intentionality"]["knowledge_encoding"]["pattern"],
        text, re.IGNORECASE
    ))
    
    functional = len(re.findall(
        STRATEGIC_PATTERNS["intentionality"]["functional_constraint"]["pattern"],
        text, re.IGNORECASE
    ))
    
    evidence = []
    
    # Strong intentionality: purpose drives form, knowledge encoded
    if (purpose_first >= STRATEGIC_PATTERNS["intentionality"]["purpose_before_form"]["threshold"] and 
        knowledge_encoding >= 1):
        evidence.extend([
            f"Found {purpose_first} purpose-before-form constructions",
            f"Found {knowledge_encoding} knowledge encoding references",
            "Intentional design: functional purpose drives structure"
        ])
        return "intentional_design", 0.85, evidence
    
    # Functional constraint-driven
    if functional >= STRATEGIC_PATTERNS["intentionality"]["functional_constraint"]["threshold"]:
        evidence.extend([
            f"Found {functional} functional constraint markers",
            "Constraint-driven: requirements shape structure"
        ])
        return "constraint_driven", 0.75, evidence
    
    # Knowledge encoding without clear purpose sequence
    if knowledge_encoding >= STRATEGIC_PATTERNS["intentionality"]["knowledge_encoding"]["threshold"]:
        evidence.append(f"Found {knowledge_encoding} knowledge encoding references")
        return "knowledge_encoding", 0.70, evidence
    
    return None, 0.0, []


def detect_symmetry_operations(text: str) -> Tuple[Optional[str], float, List[str]]:
    """Detect symmetry operation patterns in organizational structure."""
    
    rotational = len(re.findall(
        STRATEGIC_PATTERNS["symmetry_operations"]["rotational"]["pattern"],
        text, re.IGNORECASE
    ))
    
    bilateral = len(re.findall(
        STRATEGIC_PATTERNS["symmetry_operations"]["bilateral"]["pattern"],
        text, re.IGNORECASE
    ))
    
    spiral = len(re.findall(
        STRATEGIC_PATTERNS["symmetry_operations"]["spiral"]["pattern"],
        text, re.IGNORECASE
    ))
    
    evidence = []
    
    # Spiral: expanding/unfolding growth pattern
    if spiral >= STRATEGIC_PATTERNS["symmetry_operations"]["spiral"]["threshold"]:
        evidence.extend([
            f"Found {spiral} spiral/expansion markers",
            "Spiral symmetry: logarithmic growth pattern"
        ])
        return "spiral", 0.80, evidence
    
    # Rotational: circular/radial organization
    if rotational >= STRATEGIC_PATTERNS["symmetry_operations"]["rotational"]["threshold"]:
        evidence.extend([
            f"Found {rotational} rotational/radial markers",
            "Rotational symmetry: circular organization"
        ])
        return "rotational", 0.75, evidence
    
    # Bilateral: mirror/balanced structure
    if bilateral >= STRATEGIC_PATTERNS["symmetry_operations"]["bilateral"]["threshold"]:
        evidence.extend([
            f"Found {bilateral} bilateral/balance markers",
            "Bilateral symmetry: mirrored balance"
        ])
        return "bilateral", 0.75, evidence
    
    return None, 0.0, []


def detect_cultural_attribution(text: str) -> Tuple[Optional[str], float, List[str]]:
    """Detect respectful attribution vs extractive appropriation."""
    
    respectful = len(re.findall(
        STRATEGIC_PATTERNS["cultural_attribution"]["respectful_sourcing"]["pattern"],
        text, re.IGNORECASE
    ))
    
    extractive = len(re.findall(
        STRATEGIC_PATTERNS["cultural_attribution"]["extractive_language"]["pattern"],
        text, re.IGNORECASE
    ))
    
    attribution = len(re.findall(
        STRATEGIC_PATTERNS["cultural_attribution"]["attribution_markers"]["pattern"],
        text, re.IGNORECASE
    ))
    
    evidence = []
    
    # Strong respectful sourcing with attribution
    if (respectful >= STRATEGIC_PATTERNS["cultural_attribution"]["respectful_sourcing"]["threshold"] and 
        attribution >= 1):
        evidence.extend([
            f"Found {respectful} respectful sourcing markers",
            f"Found {attribution} attribution references",
            "Respectful attribution: cultural knowledge acknowledged"
        ])
        return "respectful_attribution", 0.85, evidence
    
    # Extractive language dominates
    if (extractive >= STRATEGIC_PATTERNS["cultural_attribution"]["extractive_language"]["threshold"] and 
        respectful < 2):
        evidence.extend([
            f"Found {extractive} extractive language patterns",
            f"Only {respectful} respectful markers",
            "WARNING: Extractive pattern - aesthetic borrowed without attribution"
        ])
        return "extractive_appropriation", 0.80, evidence
    
    # Attribution present but sourcing unclear
    if attribution >= STRATEGIC_PATTERNS["cultural_attribution"]["attribution_markers"]["threshold"]:
        evidence.append(f"Found {attribution} attribution markers")
        return "attribution_present", 0.65, evidence
    
    return None, 0.0, []


def analyze_strategy_document(strategy_text: str) -> dict:
    """
    Project strategy document through African Fractals structural dimensions.
    
    Detects fractal recursion patterns, scaling relationships, intentionality,
    symmetry operations, and cultural attribution in organizational structure.
    
    Zero LLM cost - pure deterministic pattern matching.
    
    Args:
        strategy_text: Full text of strategy document
    
    Returns:
        Dictionary with structural findings including:
        - dimension: structural dimension name
        - pattern: detected pattern type
        - confidence: 0.0-1.0 confidence score
        - evidence: list of supporting text patterns
        - categorical_family: objects/morphisms/constraints classification
    """
    findings = []
    text_lower = strategy_text.lower()
    
    # Run all detectors
    detectors = [
        ("recursive_structure", detect_recursive_structure, "objects"),
        ("scaling_relationship", detect_scaling_relationship, "morphisms"),
        ("intentionality", detect_intentionality, "constraints"),
        ("symmetry_operations", detect_symmetry_operations, "morphisms"),
        ("cultural_attribution", detect_cultural_attribution, "constraints"),
    ]
    
    for dimension, detector, family in detectors:
        pattern, confidence, evidence = detector(text_lower)
        if pattern and confidence > 0.6:
            findings.append({
                "dimension": dimension,
                "pattern": pattern,
                "confidence": confidence,
                "evidence": evidence,
                "categorical_family": family,
            })
    
    return {
        "domain": "african_fractals",
        "findings": findings,
        "total_findings": len(findings),
        "methodology": "deterministic_pattern_matching",
        "llm_cost_tokens": 0,
    }


@mcp.tool()
def analyze_strategy_document_tool(strategy_text: str) -> dict:
    """
    Analyze strategy document through African Fractals structural dimensions.
    
    Detects fractal recursion, scaling relationships, intentional design,
    symmetry operations, and cultural attribution patterns.
    
    Zero LLM cost - pure deterministic pattern matching.
    
    Args:
        strategy_text: Full text of the strategy document to analyze
    
    Returns:
        Dictionary with structural findings including:
        - domain: "african_fractals"
        - findings: List of detected patterns with confidence and evidence
        - total_findings: Count of findings
        - methodology: "deterministic_pattern_matching"
        - llm_cost_tokens: 0
    
    Example finding:
        {
          "dimension": "recursive_structure",
          "pattern": "fractal_recursion",
          "confidence": 0.85,
          "evidence": [
            "Found 4 nested goal structures",
            "Found 3 self-similar language patterns",
            "Fractal recursion: same principles at each scale"
          ],
          "categorical_family": "objects"
        }
    """
    return analyze_strategy_document(strategy_text)


# =============================================================================
# Entry Point


# =============================================================================
# PHASE 2.6: RHYTHMIC PRESETS — 5D MORPHOSPACE + CANONICAL STATES
# =============================================================================
#
# 5D parameter space for African Fractals aesthetic domain.
# All values normalized to [0.0, 1.0].
#
# Dimensions:
#   recursion_depth      — 0.0 (flat/minimal) → 1.0 (deep self-similar recursion)
#   symmetry_formality   — 0.0 (organic/asymmetric) → 1.0 (strict formal symmetry)
#   scaling_uniformity   — 0.0 (self-affine, variable ratios) → 1.0 (self-similar, uniform)
#   pattern_density      — 0.0 (sparse, open ground) → 1.0 (dense packed surface)
#   cultural_elaboration — 0.0 (functional/minimal) → 1.0 (maximally elaborated)
#
# Period selection strategy (cross-domain resonances):
#   30 → microscopy + diatom + heraldic   → reinforces Universal Sync attractor
#   18 → nuclear + catastrophe + diatom   → gap-filling near Period 17-19 novel attractor
#   16 → microscopy + heraldic            → enables composite beat 60 − 2×16 = 28
#   24 → microscopy (focus_sweep)         → fills 20-30 gap; harmonic of Period 12
#   12 → diatom + heraldic                → short-period LCM anchor
# =============================================================================

import numpy as np
import math

AF_PARAMETER_NAMES = [
    "recursion_depth",
    "symmetry_formality",
    "scaling_uniformity",
    "pattern_density",
    "cultural_elaboration",
]

# Canonical states derived from ethnomathematical tradition parameters.
# Each state anchors one extreme or characteristic mode of the morphospace.
AF_CANONICAL_STATES = {
    "ba_ila_settlement": {
        "coords": {
            "recursion_depth":      0.75,
            "symmetry_formality":   0.80,
            "scaling_uniformity":   0.85,
            "pattern_density":      0.25,
            "cultural_elaboration": 0.40,
        },
        "description": (
            "Concentric nested settlement rings. Open central courtyard, "
            "graduated scale reduction, clear self-similar hierarchy visible from above."
        ),
        "tradition": "ba_ila_settlements",
        "recursion_type": "scaling_iteration",
    },
    "dogon_architecture": {
        "coords": {
            "recursion_depth":      0.80,
            "symmetry_formality":   0.60,
            "scaling_uniformity":   0.60,
            "pattern_density":      0.50,
            "cultural_elaboration": 0.70,
        },
        "description": (
            "Anthropomorphic nesting of village → family compound → granary → altar. "
            "Knowledge encoded in spatial hierarchy at four scales."
        ),
        "tradition": "dogon_architecture",
        "recursion_type": "architectural_nesting",
    },
    "fulani_textile": {
        "coords": {
            "recursion_depth":      0.50,
            "symmetry_formality":   0.90,
            "scaling_uniformity":   0.70,
            "pattern_density":      0.75,
            "cultural_elaboration": 0.65,
        },
        "description": (
            "Bilateral woven geometry. Rhythmic horizontal bands of self-similar "
            "diamond motifs at multiple scales; high symmetry formality."
        ),
        "tradition": "fulani_wedding_blankets",
        "recursion_type": "self_affine_scaling",
    },
    "ethiopian_cross": {
        "coords": {
            "recursion_depth":      0.90,
            "symmetry_formality":   0.95,
            "scaling_uniformity":   0.80,
            "pattern_density":      0.85,
            "cultural_elaboration": 0.95,
        },
        "description": (
            "Maximal edge elaboration. Lattice-pierced surface, radial cross symmetry, "
            "dense interior recursion at maximum ceremonial elaboration."
        ),
        "tradition": "ethiopian_processional_crosses",
        "recursion_type": "edge_replacement",
    },
    "cornrow_spiral": {
        "coords": {
            "recursion_depth":      0.60,
            "symmetry_formality":   0.25,
            "scaling_uniformity":   0.35,
            "pattern_density":      0.55,
            "cultural_elaboration": 0.45,
        },
        "description": (
            "Logarithmic spiral recursion. Self-affine braided paths, organic asymmetry, "
            "body-scaled mathematics using transformational iteration."
        ),
        "tradition": "cornrow_hairstyles",
        "recursion_type": "transformational_iteration",
    },
    "bamana_binary": {
        "coords": {
            "recursion_depth":      0.95,
            "symmetry_formality":   0.50,
            "scaling_uniformity":   0.90,
            "pattern_density":      0.30,
            "cultural_elaboration": 0.35,
        },
        "description": (
            "Sparse binary recursion. Algorithmic divination grid, systematic bifurcation, "
            "mathematical minimalism with open ground visible."
        ),
        "tradition": "bamana_divination",
        "recursion_type": "binary_recursion",
    },
    "mangbetu_surface": {
        "coords": {
            "recursion_depth":      0.70,
            "symmetry_formality":   0.70,
            "scaling_uniformity":   0.20,
            "pattern_density":      0.90,
            "cultural_elaboration": 0.75,
        },
        "description": (
            "Dense self-affine surface tessellation. Elongated variable-ratio scaling, "
            "high surface coverage, intricate geometric fill."
        ),
        "tradition": "mangbetu_design",
        "recursion_type": "self_affine_scaling",
    },
}

# Five Phase 2.6 rhythmic presets.
# Each preset defines a periodic forced-orbit trajectory through 5D morphospace.
AF_RHYTHMIC_PRESETS = {
    "recursion_cascade": {
        "state_a": "ba_ila_settlement",
        "state_b": "ethiopian_cross",
        "pattern": "sinusoidal",
        "num_cycles": 3,
        "steps_per_cycle": 24,
        "description": (
            "Sinusoidal sweep from open nested rings (ba_ila, low density) to maximally "
            "elaborate edge recursion (ethiopian_cross, high density + elaboration). "
            "Traverses the full cultural_elaboration and recursion_depth axes."
        ),
        "period_rationale": (
            "Period 24 fills the 20-30 morphospace gap; "
            "LCM resonance with microscopy focus_sweep (period 24)."
        ),
        "dominant_axis": "cultural_elaboration + recursion_depth",
    },
    "symmetry_oscillation": {
        "state_a": "fulani_textile",
        "state_b": "cornrow_spiral",
        "pattern": "sinusoidal",
        "num_cycles": 4,
        "steps_per_cycle": 18,
        "description": (
            "Oscillation between formal bilateral textile symmetry (fulani, sf=0.90) "
            "and organic logarithmic spiral growth (cornrow, sf=0.25). "
            "Traverses symmetry_formality and scaling_uniformity together."
        ),
        "period_rationale": (
            "Period 18 resonates with nuclear + catastrophe + diatom; "
            "strengthens gap-filling attractor in the 17-19 range."
        ),
        "dominant_axis": "symmetry_formality + scaling_uniformity",
    },
    "density_wave": {
        "state_a": "bamana_binary",
        "state_b": "mangbetu_surface",
        "pattern": "triangular",
        "num_cycles": 2,
        "steps_per_cycle": 30,
        "description": (
            "Triangular wave between sparse algorithmic binary trees (bamana, pd=0.30) "
            "and dense self-affine surface elaboration (mangbetu, pd=0.90). "
            "Linear ramp captures the full pattern_density axis."
        ),
        "period_rationale": (
            "Period 30 = Universal Sync: reinforces dominant LCM attractor "
            "shared with microscopy, diatom, and heraldic domains."
        ),
        "dominant_axis": "pattern_density + cultural_elaboration",
    },
    "elaboration_pulse": {
        "state_a": "dogon_architecture",
        "state_b": "ethiopian_cross",
        "pattern": "sinusoidal",
        "num_cycles": 5,
        "steps_per_cycle": 16,
        "description": (
            "Rapid sinusoidal pulse between moderate architectural nesting "
            "(dogon, ce=0.70) and peak ceremonial edge elaboration "
            "(ethiopian_cross, ce=0.95). Drives cultural_elaboration "
            "oscillation at high frequency."
        ),
        "period_rationale": (
            "Period 16 matches microscopy contrast_pulse + heraldic; "
            "enables composite beat attractor at 60 − 2×16 = 28."
        ),
        "dominant_axis": "cultural_elaboration + recursion_depth",
    },
    "scaling_drift": {
        "state_a": "cornrow_spiral",
        "state_b": "ba_ila_settlement",
        "pattern": "square",
        "num_cycles": 4,
        "steps_per_cycle": 12,
        "description": (
            "Abrupt square-wave switch between self-affine spiral geometry "
            "(cornrow, su=0.35) and self-similar concentric rings "
            "(ba_ila, su=0.85). Highlights the scaling_uniformity axis "
            "with sharp mode transitions."
        ),
        "period_rationale": (
            "Period 12 shared with diatom + heraldic; "
            "creates short-period LCM anchors and harmonic of Period 24."
        ),
        "dominant_axis": "scaling_uniformity + symmetry_formality",
    },
}


def _af_generate_oscillation(num_steps: int, num_cycles: float, pattern: str) -> "np.ndarray":
    """Generate normalized oscillation in [0, 1]. Zero LLM cost."""
    t = np.linspace(0, 2 * math.pi * num_cycles, num_steps)
    if pattern == "sinusoidal":
        # Start at state_a (alpha=0) at t=0
        return 0.5 * (1 + np.sin(t - math.pi / 2))
    elif pattern == "triangular":
        t_norm = (t / (2 * math.pi)) % 1.0
        return np.where(t_norm < 0.5, 2 * t_norm, 2 * (1 - t_norm))
    elif pattern == "square":
        t_norm = (t / (2 * math.pi)) % 1.0
        return np.where(t_norm < 0.5, 0.0, 1.0)
    else:
        raise ValueError(f"Unknown oscillation pattern: {pattern}")


def _af_generate_preset_trajectory(preset_name: str) -> "List[Dict[str, float]]":
    """
    Generate a full preset trajectory as a list of 5D state dicts.
    Forced orbit — zero drift, guaranteed periodicity. Zero LLM cost.
    """
    preset = AF_RHYTHMIC_PRESETS[preset_name]
    coords_a = AF_CANONICAL_STATES[preset["state_a"]]["coords"]
    coords_b = AF_CANONICAL_STATES[preset["state_b"]]["coords"]
    total_steps = preset["num_cycles"] * preset["steps_per_cycle"]
    alpha = _af_generate_oscillation(total_steps, preset["num_cycles"], preset["pattern"])
    vec_a = np.array([coords_a[p] for p in AF_PARAMETER_NAMES])
    vec_b = np.array([coords_b[p] for p in AF_PARAMETER_NAMES])
    return [
        {p: float(((1 - alpha[i]) * vec_a + alpha[i] * vec_b)[j])
         for j, p in enumerate(AF_PARAMETER_NAMES)}
        for i in range(total_steps)
    ]


@mcp.tool()
def get_canonical_states() -> Dict[str, Any]:
    """
    List all canonical states in the African Fractals 5D morphospace.

    LAYER 2 — Zero LLM cost. Returns normalized parameter coordinates
    for each tradition-derived canonical state, suitable as start/end
    points for rhythmic presets or attractor visualization.

    5D dimensions:
        recursion_depth      — 0.0 (flat) → 1.0 (deep self-similar recursion)
        symmetry_formality   — 0.0 (organic asymmetric) → 1.0 (strict formal symmetry)
        scaling_uniformity   — 0.0 (self-affine, variable) → 1.0 (self-similar, uniform)
        pattern_density      — 0.0 (sparse, open) → 1.0 (dense packed surface)
        cultural_elaboration — 0.0 (functional minimal) → 1.0 (maximally elaborated)

    Returns:
        Dict with parameter_names, parameter_descriptions, states, and validation
    """
    return {
        "parameter_names": AF_PARAMETER_NAMES,
        "parameter_descriptions": {
            "recursion_depth":      "0.0 = flat/minimal recursion, 1.0 = deep self-similar recursion",
            "symmetry_formality":   "0.0 = organic/asymmetric, 1.0 = strict formal symmetry",
            "scaling_uniformity":   "0.0 = self-affine (variable ratios), 1.0 = self-similar (uniform ratios)",
            "pattern_density":      "0.0 = sparse/open ground, 1.0 = dense packed surface",
            "cultural_elaboration": "0.0 = functional/minimal, 1.0 = maximally elaborated",
        },
        "states": {
            name: {
                "coords": data["coords"],
                "description": data["description"],
                "tradition": data["tradition"],
                "recursion_type": data["recursion_type"],
            }
            for name, data in AF_CANONICAL_STATES.items()
        },
        "validation": {
            "all_params_bounded": all(
                0.0 <= v <= 1.0
                for state in AF_CANONICAL_STATES.values()
                for v in state["coords"].values()
            ),
            "state_count": len(AF_CANONICAL_STATES),
            "param_count": len(AF_PARAMETER_NAMES),
        },
    }


@mcp.tool()
def get_rhythmic_presets() -> Dict[str, Any]:
    """
    List all Phase 2.6 rhythmic presets with periods and strategic rationale.

    LAYER 2 — Zero LLM cost. Returns the 5 canonical oscillation presets
    for the African Fractals domain. Each preset defines a periodic trajectory
    using forced orbit integration (guaranteed closure, zero drift).

    Presets and periods:
        recursion_cascade    — period 24 (sinusoidal, ba_ila ↔ ethiopian_cross)
        symmetry_oscillation — period 18 (sinusoidal, fulani ↔ cornrow)
        density_wave         — period 30 (triangular, bamana ↔ mangbetu)
        elaboration_pulse    — period 16 (sinusoidal, dogon ↔ ethiopian_cross)
        scaling_drift        — period 12 (square, cornrow ↔ ba_ila)

    Returns:
        Dict with preset definitions, period summary, and cross-domain resonance map
    """
    return {
        "domain": "african_fractals",
        "phase": "2.6",
        "parameter_names": AF_PARAMETER_NAMES,
        "presets": {
            name: {
                "state_a": preset["state_a"],
                "state_b": preset["state_b"],
                "pattern": preset["pattern"],
                "period": preset["steps_per_cycle"],
                "num_cycles": preset["num_cycles"],
                "total_steps": preset["num_cycles"] * preset["steps_per_cycle"],
                "description": preset["description"],
                "period_rationale": preset["period_rationale"],
                "dominant_axis": preset["dominant_axis"],
            }
            for name, preset in AF_RHYTHMIC_PRESETS.items()
        },
        "period_summary": {
            name: preset["steps_per_cycle"]
            for name, preset in AF_RHYTHMIC_PRESETS.items()
        },
        "cross_domain_resonances": {
            "period_30": ["microscopy", "diatom", "heraldic", "african_fractals:density_wave"],
            "period_18": ["nuclear", "catastrophe", "diatom", "african_fractals:symmetry_oscillation"],
            "period_16": ["microscopy", "heraldic", "african_fractals:elaboration_pulse"],
            "period_24": ["microscopy", "african_fractals:recursion_cascade"],
            "period_12": ["diatom", "heraldic", "african_fractals:scaling_drift"],
        },
    }


@mcp.tool()
def apply_rhythmic_preset(
    preset_name: str,
    phase_position: float = 0.0,
) -> Dict[str, Any]:
    """
    Apply a Phase 2.6 rhythmic preset and return the 5D state at a given phase.

    LAYER 2 — Deterministic forced orbit, zero LLM cost. Phase advances
    uniformly along the preset trajectory, guaranteeing periodic closure
    with zero numerical drift.

    Args:
        preset_name: One of the 5 presets:
            "recursion_cascade"    — period 24, sinusoidal, ba_ila ↔ ethiopian_cross
            "symmetry_oscillation" — period 18, sinusoidal, fulani ↔ cornrow
            "density_wave"         — period 30, triangular, bamana ↔ mangbetu
            "elaboration_pulse"    — period 16, sinusoidal, dogon ↔ ethiopian_cross
            "scaling_drift"        — period 12, square, cornrow ↔ ba_ila
        phase_position: Phase in [0.0, 1.0) — fractional position in one cycle.
            0.0 → state_a coordinates, 0.5 → midpoint, 1.0 → back to state_a.

    Returns:
        Current 5D state, alpha (interpolation weight), nearest canonical state,
        period, and dominant axis metadata
    """
    if preset_name not in AF_RHYTHMIC_PRESETS:
        available = ", ".join(AF_RHYTHMIC_PRESETS.keys())
        return {"error": f"Preset '{preset_name}' not found. Available: {available}"}

    phase_position = max(0.0, min(1.0, float(phase_position)))
    preset = AF_RHYTHMIC_PRESETS[preset_name]
    coords_a = AF_CANONICAL_STATES[preset["state_a"]]["coords"]
    coords_b = AF_CANONICAL_STATES[preset["state_b"]]["coords"]

    t = phase_position * 2 * math.pi
    pattern = preset["pattern"]
    if pattern == "sinusoidal":
        alpha = 0.5 * (1 + math.sin(t - math.pi / 2))
    elif pattern == "triangular":
        tn = phase_position % 1.0
        alpha = 2 * tn if tn < 0.5 else 2 * (1 - tn)
    elif pattern == "square":
        alpha = 0.0 if phase_position < 0.5 else 1.0
    else:
        alpha = phase_position

    vec_a = np.array([coords_a[p] for p in AF_PARAMETER_NAMES])
    vec_b = np.array([coords_b[p] for p in AF_PARAMETER_NAMES])
    current = (1 - alpha) * vec_a + alpha * vec_b
    state = {p: float(current[i]) for i, p in enumerate(AF_PARAMETER_NAMES)}

    # Nearest canonical state
    min_dist, nearest = float("inf"), None
    for sname, sdata in AF_CANONICAL_STATES.items():
        ref = np.array([sdata["coords"][p] for p in AF_PARAMETER_NAMES])
        d = float(np.linalg.norm(current - ref))
        if d < min_dist:
            min_dist, nearest = d, sname

    return {
        "preset": preset_name,
        "phase_position": phase_position,
        "alpha": round(float(alpha), 4),
        "state": state,
        "period": preset["steps_per_cycle"],
        "pattern": preset["pattern"],
        "interpolating_between": {
            "state_a": preset["state_a"],
            "state_b": preset["state_b"],
        },
        "nearest_canonical_state": {
            "name": nearest,
            "distance": round(min_dist, 4),
        },
        "dominant_axis": preset["dominant_axis"],
    }


# =============================================================================
# PHASE 2.7: ATTRACTOR VISUALIZATION PROMPT GENERATION
# =============================================================================
#
# Five visual types spanning the 5D morphospace.
# Nearest-neighbor lookup (Euclidean distance) selects vocabulary.
# Distance-weighted blending produces composite keywords.
# Zero LLM cost — pure deterministic extraction.
# =============================================================================

AF_VISUAL_TYPES = {
    "settlement_rings": {
        "coords": {
            "recursion_depth":      0.75,
            "symmetry_formality":   0.80,
            "scaling_uniformity":   0.85,
            "pattern_density":      0.25,
            "cultural_elaboration": 0.40,
        },
        "keywords": [
            "concentric settlement rings",
            "nested circular compounds",
            "open central courtyard",
            "graduated scale reduction",
            "aerial village topology",
            "self-similar ring clusters",
            "geometric containment",
        ],
        "prompt_style": "aerial geometric, architectural overhead",
        "tradition_anchor": "ba_ila_settlements",
    },
    "textile_weave": {
        "coords": {
            "recursion_depth":      0.50,
            "symmetry_formality":   0.90,
            "scaling_uniformity":   0.70,
            "pattern_density":      0.75,
            "cultural_elaboration": 0.65,
        },
        "keywords": [
            "bilateral woven geometry",
            "repeating diamond lattice",
            "rhythmic horizontal bands",
            "high-contrast thread patterns",
            "iterative loom structure",
            "plaited surface texture",
            "ceremonial textile precision",
        ],
        "prompt_style": "textile close-up, woven surface pattern",
        "tradition_anchor": "fulani_wedding_blankets",
    },
    "binary_tree": {
        "coords": {
            "recursion_depth":      0.95,
            "symmetry_formality":   0.50,
            "scaling_uniformity":   0.90,
            "pattern_density":      0.30,
            "cultural_elaboration": 0.35,
        },
        "keywords": [
            "branching binary recursion",
            "sparse algorithmic structure",
            "divination grid layout",
            "systematic bifurcation nodes",
            "open ground between branches",
            "decision tree geometry",
            "mathematical minimalism",
        ],
        "prompt_style": "mathematical diagram, algorithmic structure",
        "tradition_anchor": "bamana_divination",
    },
    "edge_elaboration": {
        "coords": {
            "recursion_depth":      0.90,
            "symmetry_formality":   0.95,
            "scaling_uniformity":   0.80,
            "pattern_density":      0.85,
            "cultural_elaboration": 0.95,
        },
        "keywords": [
            "ornate edge replacement iteration",
            "lattice-pierced metalwork surface",
            "maximum ceremonial elaboration",
            "radial cross symmetry",
            "dense interior geometric fill",
            "precious filigree quality",
            "sacred recursive complexity",
        ],
        "prompt_style": "metalwork, ceremonial object, close detail",
        "tradition_anchor": "ethiopian_processional_crosses",
    },
    "spiral_growth": {
        "coords": {
            "recursion_depth":      0.60,
            "symmetry_formality":   0.25,
            "scaling_uniformity":   0.35,
            "pattern_density":      0.55,
            "cultural_elaboration": 0.45,
        },
        "keywords": [
            "logarithmic spiral curves",
            "organic flowing recursion",
            "asymmetric growth trajectory",
            "self-affine elongated path",
            "braided kinetic texture",
            "body-scaled mathematics",
            "transformational iteration",
        ],
        "prompt_style": "organic curve, kinetic line",
        "tradition_anchor": "cornrow_hairstyles",
    },
}


def _af_nearest_visual_type(state: "Dict[str, float]") -> "Tuple[str, float]":
    """Nearest visual type by Euclidean distance in 5D. Zero LLM cost."""
    current = np.array([state.get(p, 0.5) for p in AF_PARAMETER_NAMES])
    dists = [
        (name, float(np.linalg.norm(
            current - np.array([data["coords"][p] for p in AF_PARAMETER_NAMES])
        )))
        for name, data in AF_VISUAL_TYPES.items()
    ]
    dists.sort(key=lambda x: x[1])
    return dists[0][0], dists[0][1]


def _af_weighted_keywords(state: "Dict[str, float]", max_keywords: int = 6) -> "List[str]":
    """Distance-weighted keyword extraction across all visual types. Zero LLM cost."""
    current = np.array([state.get(p, 0.5) for p in AF_PARAMETER_NAMES])
    dists = sorted(
        [
            (name, float(np.linalg.norm(
                current - np.array([data["coords"][p] for p in AF_PARAMETER_NAMES])
            )))
            for name, data in AF_VISUAL_TYPES.items()
        ],
        key=lambda x: x[1],
    )
    keywords, seen = [], set()
    for name, dist in dists:
        weight = max(0.0, 1.0 - dist / 1.5)
        if weight < 0.15:
            break
        n_from = max(1, round(weight * 3))
        for kw in AF_VISUAL_TYPES[name]["keywords"][:n_from]:
            if kw not in seen:
                keywords.append(kw)
                seen.add(kw)
        if len(keywords) >= max_keywords:
            break
    return keywords[:max_keywords]


@mcp.tool()
def get_visual_types() -> Dict[str, Any]:
    """
    List all Phase 2.7 visual types in the African Fractals domain.

    LAYER 2 — Zero LLM cost. Returns the 5 canonical visual types with
    their 5D morphospace coordinates and image-generation keywords.
    Nearest-neighbor matching selects vocabulary for any arbitrary state.

    Visual types:
        settlement_rings  — open self-similar, low density, high scaling uniformity
        textile_weave     — formal bilateral, medium depth, high density
        binary_tree       — maximal recursion depth, sparse, minimal elaboration
        edge_elaboration  — peak elaboration, dense surface, maximum symmetry
        spiral_growth     — organic asymmetric, self-affine, medium density

    Returns:
        Dict with visual type definitions, coords, keywords, and self-match validation
    """
    return {
        "domain": "african_fractals",
        "phase": "2.7",
        "parameter_names": AF_PARAMETER_NAMES,
        "visual_types": {
            name: {
                "coords": data["coords"],
                "keywords": data["keywords"],
                "prompt_style": data["prompt_style"],
                "tradition_anchor": data["tradition_anchor"],
            }
            for name, data in AF_VISUAL_TYPES.items()
        },
        "validation": {
            "self_match_distances": {
                name: round(_af_nearest_visual_type(data["coords"])[1], 6)
                for name, data in AF_VISUAL_TYPES.items()
            },
            "all_params_bounded": all(
                0.0 <= v <= 1.0
                for vt in AF_VISUAL_TYPES.values()
                for v in vt["coords"].values()
            ),
        },
    }


@mcp.tool()
def get_visual_vocabulary(
    state: Optional[Dict[str, float]] = None,
    preset_name: Optional[str] = None,
    phase_position: float = 0.0,
) -> Dict[str, Any]:
    """
    Extract visual vocabulary keywords from a 5D state or preset phase position.

    LAYER 2 — Zero LLM cost. Nearest-neighbor search identifies the closest
    visual type; distance-weighted blending produces composite keywords for
    image generation prompts.

    Provide EITHER a state dict OR a preset_name (with optional phase_position).

    Args:
        state: 5D dict with keys: recursion_depth, symmetry_formality,
               scaling_uniformity, pattern_density, cultural_elaboration.
               All values [0.0, 1.0]. If None, preset_name must be given.
        preset_name: Phase 2.6 preset to sample (overrides state if both given).
        phase_position: Phase in [0.0, 1.0) when using preset_name.

    Returns:
        Nearest visual type, distance, ranked type list, weighted keywords,
        and nearest type metadata
    """
    if preset_name is not None:
        pr = apply_rhythmic_preset(preset_name, phase_position)
        if "error" in pr:
            return pr
        resolved = pr["state"]
        source = f"preset:{preset_name}@{phase_position:.3f}"
    elif state is not None:
        resolved = state
        source = "provided_state"
    else:
        return {"error": "Provide either 'state' or 'preset_name'."}

    nearest_type, distance = _af_nearest_visual_type(resolved)
    keywords = _af_weighted_keywords(resolved, max_keywords=7)
    current = np.array([resolved.get(p, 0.5) for p in AF_PARAMETER_NAMES])
    ranked = sorted(
        [
            (t, float(np.linalg.norm(
                current - np.array([d["coords"][p] for p in AF_PARAMETER_NAMES])
            )))
            for t, d in AF_VISUAL_TYPES.items()
        ],
        key=lambda x: x[1],
    )

    return {
        "state": resolved,
        "state_source": source,
        "nearest_visual_type": nearest_type,
        "distance_to_nearest": round(distance, 4),
        "visual_type_ranking": [{"type": t, "distance": round(d, 4)} for t, d in ranked],
        "weighted_keywords": keywords,
        "nearest_type_metadata": {
            "prompt_style": AF_VISUAL_TYPES[nearest_type]["prompt_style"],
            "tradition_anchor": AF_VISUAL_TYPES[nearest_type]["tradition_anchor"],
            "full_keywords": AF_VISUAL_TYPES[nearest_type]["keywords"],
        },
    }


@mcp.tool()
def generate_attractor_prompt(
    state: Optional[Dict[str, float]] = None,
    preset_name: Optional[str] = None,
    phase_position: float = 0.0,
    mode: str = "composite",
    target_generator: str = "stable_diffusion",
    include_negative: bool = True,
) -> Dict[str, Any]:
    """
    Generate an image generation prompt from a 5D attractor state or preset phase.

    LAYER 2/3 boundary — vocabulary extraction is zero LLM cost (Layer 2);
    structured prompt data is returned for Claude synthesis (Layer 3).

    Provide EITHER a state dict OR a preset_name (with optional phase_position).

    Args:
        state: 5D parameter dict. Keys: recursion_depth, symmetry_formality,
               scaling_uniformity, pattern_density, cultural_elaboration.
               All values [0.0, 1.0].
        preset_name: Phase 2.6 preset to sample. Overrides state if provided.
        phase_position: Phase in [0.0, 1.0) when using preset_name.
        mode: Prompt generation strategy:
            "composite"  — single blended prompt (default, best for most generators)
            "split_view" — separate keyword sets per dominant visual type
            "sequence"   — keyframe prompts across one full preset cycle
                           (requires preset_name)
        target_generator: "stable_diffusion" | "dalle" | "comfyui" | "midjourney"
        include_negative: Whether to include negative prompt guidance.

    Returns:
        Structured prompt data with keywords, parameter qualifiers,
        mode-specific output, and (optionally) negative prompt
    """
    # Resolve state
    if preset_name is not None:
        pr = apply_rhythmic_preset(preset_name, phase_position)
        if "error" in pr:
            return pr
        resolved = pr["state"]
        source = f"preset:{preset_name}@{phase_position:.3f}"
        period = pr["period"]
    elif state is not None:
        resolved = state
        source = "provided_state"
        period = None
    else:
        return {"error": "Provide either 'state' or 'preset_name'."}

    vocab = get_visual_vocabulary(state=resolved)
    nearest_type = vocab["nearest_visual_type"]
    keywords = vocab["weighted_keywords"]

    # Parameter-driven qualifiers for prompt richness
    rd = resolved.get("recursion_depth", 0.5)
    sf = resolved.get("symmetry_formality", 0.5)
    su = resolved.get("scaling_uniformity", 0.5)
    pd_ = resolved.get("pattern_density", 0.5)
    ce = resolved.get("cultural_elaboration", 0.5)

    qualifiers = {
        "recursion_depth": (
            "subtle recursive layering" if rd < 0.4
            else "clear fractal hierarchy" if rd < 0.7
            else "deep self-similar recursion"
        ),
        "symmetry_formality": (
            "organic asymmetric flow" if sf < 0.35
            else "balanced bilateral structure" if sf < 0.70
            else "strict formal symmetry"
        ),
        "scaling_uniformity": (
            "self-affine variable ratios" if su < 0.40
            else "proportional scaling" if su < 0.70
            else "uniform self-similar scaling"
        ),
        "pattern_density": (
            "sparse open ground" if pd_ < 0.35
            else "medium pattern coverage" if pd_ < 0.65
            else "dense packed surface"
        ),
        "cultural_elaboration": (
            "functional geometric clarity" if ce < 0.40
            else "rich cultural ornament" if ce < 0.75
            else "maximal ceremonial elaboration"
        ),
    }

    style_tags = {
        "stable_diffusion": (
            "((African fractal mathematics)), ethnomathematical design, "
            "intentional geometry, detailed, sharp focus, 8k"
        ),
        "dalle": "African fractal design with intentional mathematical structure,",
        "comfyui": "african_fractal_mathematics, ethnomathematical, intentional_geometry",
        "midjourney": "African fractal mathematics, ethnomathematical geometry --style raw --ar 1:1",
    }
    style_suffix = style_tags.get(target_generator, style_tags["stable_diffusion"])
    negative = (
        "generic tribal, primitive, accidental pattern, machine-perfect without variation, "
        "decorative only, no mathematical structure, mixed traditions, blurry, low quality"
    )

    # Mode dispatch
    if mode == "composite":
        prompt = (
            f"{', '.join(keywords)}, "
            f"{qualifiers['recursion_depth']}, {qualifiers['symmetry_formality']}, "
            f"{qualifiers['pattern_density']}, {qualifiers['cultural_elaboration']}, "
            f"{style_suffix}"
        )
        mode_output = {
            "mode": "composite",
            "prompt": prompt,
            "keywords_used": keywords,
            "nearest_visual_type": nearest_type,
        }

    elif mode == "split_view":
        top2 = vocab["visual_type_ranking"][:2]
        split = {}
        for entry in top2:
            t = entry["type"]
            t_kw = AF_VISUAL_TYPES[t]["keywords"][:4]
            split[t] = {
                "prompt": f"{', '.join(t_kw)}, {AF_VISUAL_TYPES[t]['prompt_style']}, {style_suffix}",
                "prompt_style": AF_VISUAL_TYPES[t]["prompt_style"],
                "tradition": AF_VISUAL_TYPES[t]["tradition_anchor"],
                "distance": entry["distance"],
            }
        mode_output = {
            "mode": "split_view",
            "split_prompts": split,
            "composite_modifiers": qualifiers,
        }

    elif mode == "sequence":
        if preset_name is None:
            return {"error": "mode='sequence' requires preset_name."}
        n_kf = min(AF_RHYTHMIC_PRESETS[preset_name]["steps_per_cycle"], 8)
        keyframes = []
        for i in range(n_kf):
            ph = i / n_kf
            kf_pr = apply_rhythmic_preset(preset_name, ph)
            kf_vocab = get_visual_vocabulary(state=kf_pr["state"])
            kf_kw = kf_vocab["weighted_keywords"][:4]
            keyframes.append({
                "keyframe": i,
                "phase": round(ph, 3),
                "nearest_type": kf_vocab["nearest_visual_type"],
                "prompt": f"{', '.join(kf_kw)}, {style_suffix}",
                "state": kf_pr["state"],
            })
        mode_output = {
            "mode": "sequence",
            "preset": preset_name,
            "period": period,
            "keyframe_count": n_kf,
            "keyframes": keyframes,
        }

    else:
        return {"error": f"Unknown mode '{mode}'. Use: composite, split_view, sequence"}

    # Common fields
    mode_output.update({
        "state": resolved,
        "state_source": source,
        "target_generator": target_generator,
        "parameter_qualifiers": qualifiers,
    })
    if include_negative:
        mode_output["negative_prompt"] = negative
    if period:
        mode_output["period"] = period
        mode_output["period_rationale"] = AF_RHYTHMIC_PRESETS[preset_name]["period_rationale"]

    return mode_output


@mcp.tool()
def get_domain_registry_config() -> Dict[str, Any]:
    """
    Export African Fractals domain configuration for the Lushy composition registry.

    LAYER 2 — Zero LLM cost. Returns the complete domain specification for
    registering african_fractals in the emergent attractor discovery system
    (domain_registry.py, Tier 4D). Includes preset periods, parameter names,
    state coordinates, visual vocabulary, and cross-domain resonance map.

    Returns:
        DomainConfig-compatible dict ready for register_african_fractals()
    """
    return {
        "domain_id": "african_fractals",
        "display_name": "African Fractal Mathematics",
        "description": (
            "Ethnomathematical fractal aesthetics from African design traditions. "
            "Based on Ron Eglash's research documenting intentional mathematical "
            "knowledge encoded in settlements, textiles, hairstyles, ceremonial "
            "objects, and architectural forms."
        ),
        "mcp_server": "african-fractals",
        "phase_2_6_complete": True,
        "phase_2_7_complete": True,
        "parameter_names": AF_PARAMETER_NAMES,
        "presets": {
            name: {
                "period": preset["steps_per_cycle"],
                "pattern": preset["pattern"],
                "state_a_id": preset["state_a"],
                "state_b_id": preset["state_b"],
                "description": preset["description"],
            }
            for name, preset in AF_RHYTHMIC_PRESETS.items()
        },
        "preset_periods": sorted([p["steps_per_cycle"] for p in AF_RHYTHMIC_PRESETS.values()]),
        "state_coordinates": {
            name: data["coords"]
            for name, data in AF_CANONICAL_STATES.items()
        },
        "visual_types": {
            name: {
                "coords": data["coords"],
                "keywords": data["keywords"],
                "prompt_style": data["prompt_style"],
            }
            for name, data in AF_VISUAL_TYPES.items()
        },
        "cross_domain_resonances": {
            "period_12": {
                "domains": ["diatom", "heraldic"],
                "preset": "scaling_drift",
                "mechanism": "Short-period LCM anchor; harmonic of period 24",
            },
            "period_16": {
                "domains": ["microscopy", "heraldic"],
                "preset": "elaboration_pulse",
                "mechanism": "Enables composite beat 60 − 2×16 = 28",
            },
            "period_18": {
                "domains": ["nuclear", "catastrophe", "diatom"],
                "preset": "symmetry_oscillation",
                "mechanism": "Gap-filling near novel Period 17-19 attractor",
            },
            "period_24": {
                "domains": ["microscopy"],
                "preset": "recursion_cascade",
                "mechanism": "Fills 20-30 gap; harmonic of period 12",
            },
            "period_30": {
                "domains": ["microscopy", "diatom", "heraldic"],
                "preset": "density_wave",
                "mechanism": "Universal Sync — reinforces dominant multi-domain LCM attractor",
            },
        },
        "predicted_emergent_attractors": [
            {
                "period": 30,
                "classification": "lcm_sync",
                "basis": "density_wave(30) × microscopy(30) × diatom(30) × heraldic(30) — 4-domain reinforcement",
                "expected_basin": ">10%",
            },
            {
                "period": 18,
                "classification": "novel_gap_filler",
                "basis": "symmetry_oscillation(18) reinforces Period 17-19 gap attractor with nuclear/catastrophe/diatom",
                "expected_basin": "5-8%",
            },
            {
                "period": 24,
                "classification": "novel_gap_filler",
                "basis": "recursion_cascade(24) fills 20-30 gap; not LCM of common periods",
                "expected_basin": "3-6%",
            },
            {
                "period": 28,
                "classification": "composite_beat",
                "basis": "Period 60 hub − 2 × elaboration_pulse(16) = 28; maintains fragile mechanism",
                "expected_basin": "2-4% (fragile, domain-count sensitive)",
            },
        ],
        "validation": {
            "canonical_state_count": len(AF_CANONICAL_STATES),
            "preset_count": len(AF_RHYTHMIC_PRESETS),
            "visual_type_count": len(AF_VISUAL_TYPES),
            "all_canonical_params_bounded": all(
                0.0 <= v <= 1.0
                for s in AF_CANONICAL_STATES.values()
                for v in s["coords"].values()
            ),
            "all_visual_type_params_bounded": all(
                0.0 <= v <= 1.0
                for vt in AF_VISUAL_TYPES.values()
                for v in vt["coords"].values()
            ),
            "visual_type_self_match_distances": {
                name: round(_af_nearest_visual_type(data["coords"])[1], 6)
                for name, data in AF_VISUAL_TYPES.items()
            },
        },
    }


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == '__main__':
    mcp.run()
