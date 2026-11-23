// ONE DAY ON EARTH — Sunday 22 November 2026.
// Node 22, standard library only. The front page is pre-drawn (entry.png,
// 1024x1024, PIL) and this program copies it to the output directory after
// checking it is a real PNG within the 1 MiB gate, then writes a small
// deterministic dossier.json describing the entry.
//
//   MAKEFUN_OUTPUT_DIR=out node main.ts
import { createHash } from "node:crypto";
import { copyFileSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// --- read and validate entry.png ---
const buf = readFileSync(src);
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!buf.subarray(0, 8).equals(PNG_SIG)) {
  throw new Error("entry.png is not a PNG");
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png must be 1024x1024, got ${width}x${height}`);
}
const size = statSync(src).size;
if (size > 1_048_576) {
  throw new Error(`entry.png exceeds 1,048,576 bytes (got ${size})`);
}
// --- walk the PNG chunks and verify every CRC (the gate wants a whole
// image: every chunk with its checksum and the data its header describes).
const CRC_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[n] = c >>> 0;
  }
  return table;
})();
function crc32(bytes) {
  let c = 0xffffffff;
  for (const b of bytes) c = CRC_TABLE[(c ^ b) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}
let off = 8;
let sawIEND = false;
while (off + 8 <= buf.length) {
  const len = buf.readUInt32BE(off);
  const type = buf.toString("ascii", off + 4, off + 8);
  if (off + 12 + len > buf.length) throw new Error(`PNG chunk ${type} is truncated`);
  const stored = buf.readUInt32BE(off + 8 + len);
  const actual = crc32(buf.subarray(off + 4, off + 8 + len));
  if (stored !== actual) throw new Error(`PNG chunk ${type} has a bad CRC`);
  off += 12 + len;
  if (type === "IEND") {
    sawIEND = true;
    break;
  }
}
if (!sawIEND) throw new Error("PNG has no IEND chunk");
if (off !== buf.length) throw new Error("trailing bytes after PNG IEND");

// --- copy + dossier (no timestamps: byte-identical across runs) ---
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
const sha256 = createHash("sha256").update(buf).digest("hex");
const dossier = {
  competition: "news-image-20261122",
  title: "ONE DAY ON EARTH — Sunday 22 November 2026",
  stories: 35,
  regions: 6,
  pictured: 13,
  entry: { file: "entry.png", width, height, bytes: size, sha256 },
  generator: "draw.py (PIL, stdlib-only main.ts)",
};
writeFileSync(join(outDir, "dossier.json"), JSON.stringify(dossier, null, 2) + "\n");
console.log(`copied entry.png (${size} bytes, sha256 ${sha256.slice(0, 16)}…)`);
