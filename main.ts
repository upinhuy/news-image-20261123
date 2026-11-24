// Entry program for news-image-20261123 ("World news, 23 November 2026").
//
// The image is drawn once, by hand, in draw.py and committed as entry.png.
// This program only copies that committed image to the output directory.
// It uses Node's standard library only: no network, no child processes,
// no rendering at runtime, so both grader runs write identical bytes.

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(here, "entry.png");
const dest = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);

// Fail loudly instead of silently shipping a partial copy.
if (statSync(src).size !== statSync(dest).size) {
  throw new Error("entry.png copy size mismatch");
}
