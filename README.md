# African Fractals MCP Server

A Lushy brick encoding African fractal design traditions as visual vocabulary for AI image generation, based on Ron Eglash's ethnomathematical research.

## Attribution

This vocabulary draws from:
- **Primary Source**: "African Fractals: Modern Computing and Indigenous Design" by Ron Eglash (1999)
- **Core Insight**: African fractal designs encode intentional mathematical knowledge—recursion, scaling algorithms, and self-similarity developed for cosmological, practical, and social purposes

## Why Cultural Specificity Matters

This brick treats each tradition as a distinct mathematical knowledge system, not interchangeable variations of a generic "African style":

| Tradition | Culture | Region | Recursion Type |
|-----------|---------|--------|----------------|
| Ba-ila Settlements | Ba-ila | Zambia | Cellular nesting |
| Dogon Architecture | Dogon | Mali | Cellular nesting |
| Fulani Wedding Blankets | Fulani | West Africa | Self-affine |
| Ethiopian Crosses | Ethiopian Orthodox | Ethiopia | Iterative elaboration |
| Akan Goldweights | Akan | Ghana | Self-similar exact |
| Bamana Divination | Bamana | Mali | Binary recursion |
| Mangbetu Design | Mangbetu | DRC | Self-affine |

## Installation

```bash
cd african-fractals-olog
pip install -e .
```

## Claude Desktop Configuration

```json
{
  "mcpServers": {
    "african-fractals": {
      "command": "python",
      "args": ["/path/to/african-fractals-olog/server.py"]
    }
  }
}
```

## Tools

### Layer 1: Taxonomy Lookup (Zero LLM Cost)

- `list_traditions()` - All available traditions with cultural attribution
- `get_tradition_profile(tradition_name)` - Complete profile for one tradition
- `list_recursion_types()` - Recursion mechanisms with visual signatures
- `list_symmetry_modes()` - Symmetry-recursion interactions
- `get_intentionality_principles()` - Why these patterns work

### Layer 2: Deterministic Mapping (Zero LLM Cost)

- `map_intent_to_tradition(intent)` - Map creative intent to recommended tradition
- `build_visual_parameters(tradition_name, ...)` - Complete parameter set

### Layer 3: Synthesis Support

- `enhance_with_african_fractals(base_prompt, tradition_name, ...)` - Full enhancement data
- `get_composition_guidance(other_domain)` - Guidance for composing with other bricks
- `get_example_compositions()` - Complete worked examples

## Usage Examples

### Basic Enhancement

```
User: "A meditation space with fractal patterns"

Claude calls: enhance_with_african_fractals(
    base_prompt="A meditation space with fractal patterns",
    tradition_name="ba_ila_settlements",
    intent="contained_complexity",
    recursion_depth=3
)
```

### Composing with Other Domains

```
User: "Jazz-inspired fractal visualization"

Claude calls:
1. get_composition_guidance("jazz")
2. jazz-improvisation:encode_ii_V_I_monoid(...)
3. enhance_with_african_fractals(...) 
4. Synthesize combined parameters
```

## Core Principles

### Recursion Types Map to Different Feelings

- **Cellular nesting** (Ba-ila): Containment, protection, hierarchy
- **Iterative elaboration** (Ethiopian crosses): Wonder, infinite depth
- **Self-affine** (Fulani textiles): Rhythm, journey, accumulation
- **Branching**: Organic growth, living systems
- **Binary recursion** (Bamana): Decision, fate, hidden knowledge

### Scale Encodes Meaning

- In social patterns: Larger = more important
- In sacred patterns: Smaller = deeper contemplation
- In textile patterns: Scale variation = rhythmic interest

### Deliberate Imperfection

Many traditions include intentional irregularity—humility before the divine, authentication of human origin, prevention of trapped spirits. Perfect machine regularity often feels wrong.

### Material Shapes Expression

Each tradition developed in specific media. Woven textiles have stepped diagonals. Mud architecture curves. Cast metal shows casting texture. Rendering should reference actual materials.

## Composition Compatibility

| Domain | Connection | Strategy |
|--------|------------|----------|
| Origami | Recursive folding ↔ recursive scaling | Origami as medium for fractal expression |
| Jazz | Nested musical ↔ nested visual scales | Musical recursion informing visual rhythm |
| Genetic | Biological ↔ cultural fractals | Nature-culture fractal dialogue |
| Grid Dynamics | Regular grid vs fractal subdivision | Grid as scaffold for fractal growth |

## File Structure

```
african-fractals-olog/
├── african_fractals.olog.yaml  # Complete categorical specification
├── INTENTIONALITY.md           # Why these aesthetic choices work
├── server.py                   # MCP server implementation
├── pyproject.toml             # Package configuration
└── README.md                  # This file
```

## The Intentionality Test

Generated imagery succeeds when it could answer:
1. **What tradition does this represent?** (Specific answer, not "African")
2. **What recursion type is operating?** (Identifiable algorithm)
3. **Why this material rendering?** (Matches tradition's actual media)
4. **What does scale encode here?** (Hierarchy, rhythm, depth, etc.)
5. **Where is the intentional imperfection?** (Authentication through irregularity)

## Further Reading

- Eglash, Ron. *African Fractals: Modern Computing and Indigenous Design*. Rutgers University Press, 1999.
- [Culturally Situated Design Tools](https://csdt.org/) - Interactive simulations based on Eglash's research
- [Ron Eglash's TED Talk](https://www.ted.com/talks/ron_eglash_the_fractals_at_the_heart_of_african_designs)

## License

MIT License. Cultural knowledge belongs to its source communities—this tool facilitates respectful engagement, not appropriation.
