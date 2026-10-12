# Play frame

The five painted pieces of the game screen's frame. They are the engine's own, the same in every narrative, and show nothing of any world.

| File | What it is | Size |
|---|---|---|
| `Ground.webp` | Honed black stone, the ground round the page | 1024 × 1024, tiles both ways |
| `Ledger.webp` | Dark patinated bronze, the ledger's ground | 1024 × 1024, tiles both ways |
| `Rail.png` | An old-gilt rail, lit from above | 1024 × 40, tiles end to end, alpha above and below |
| `Boss.png` | An obsidian diamond in a gilt bezel, seated on the rail | 240 × 96, alpha |
| `Corner.png` | A flat gilt corner bracket, the top-left one | 128 × 128, alpha |

The `/frame` route serves these five names and no others, so a replacement keeps its name and format. Any of them may be absent: the game screen then draws that part itself. A changed file is seen the next time the window is opened.
