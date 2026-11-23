// ONE DAY ON EARTH — Sunday 22 November 2026.
// Node 22, standard library only. The front page artwork is pre-rendered
// (entry.png, 1024x1024, drawn by draw.py) and this program is the gate
// between the artwork and the output directory: it checks the PNG is whole
// and inside the 1 MiB limit, copies it over, and writes a small
// deterministic dossier.json describing the entry.
//
//   MAKEFUN_OUTPUT_DIR=out node main.ts
import { createHash } from "node:crypto";
import { copyFileSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC_HEX = "89504e470d0a1a0a";
const PAGE_SIDE = 1024;
const BYTE_LIMIT = 1_048_576;

const here = dirname(fileURLToPath(import.meta.url));
const sourcePng = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

function die(message) {
  throw new Error(message);
}

function checkMagic(buf) {
  if (buf.toString("hex", 0, 8) !== PNG_MAGIC_HEX) die("entry.png is not a PNG");
}

function readDimensions(buf) {
  const width = buf.readUInt32BE(16);
  const height = buf.readUInt32BE(20);
  if (width !== PAGE_SIDE || height !== PAGE_SIDE) {
    die(`entry.png must be 1024x1024, got ${width}x${height}`);
  }
  return { width, height };
}

function checkSize(bytes) {
  if (bytes > BYTE_LIMIT) {
    die(`entry.png exceeds 1,048,576 bytes (got ${bytes})`);
  }
}

function buildCrcTable() {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) {
      c = (c & 1) === 0 ? c >>> 1 : 0xedb88320 ^ (c >>> 1);
    }
    table[n] = c >>> 0;
  }
  return table;
}
const CRC_TABLE = buildCrcTable();

function crc32(bytes) {
  let c = 0xffffffff;
  for (let i = 0; i < bytes.length; i++) {
    c = CRC_TABLE[(c ^ bytes[i]) & 0xff] ^ (c >>> 8);
  }
  return (c ^ 0xffffffff) >>> 0;
}

// Walk the PNG chunks and verify every CRC, so the gate only passes a
// whole image: every chunk with its checksum and the data its header
// describes.
function walkChunks(buf) {
  let offset = 8;
  let sawIEND = false;
  while (offset + 8 <= buf.length) {
    const length = buf.readUInt32BE(offset);
    const type = buf.toString("ascii", offset + 4, offset + 8);
    if (offset + 12 + length > buf.length) die(`PNG chunk ${type} is truncated`);
    const stored = buf.readUInt32BE(offset + 8 + length);
    const actual = crc32(buf.subarray(offset + 4, offset + 8 + length));
    if (stored !== actual) die(`PNG chunk ${type} has a bad CRC`);
    offset += 12 + length;
    if (type === "IEND") {
      sawIEND = true;
      break;
    }
  }
  if (!sawIEND) die("PNG has no IEND chunk");
  if (offset !== buf.length) die("trailing bytes after PNG IEND");
}

function buildDossier(width, height, size, sha256) {
  return {
    competition: "news-image-20261122",
    title: "ONE DAY ON EARTH — Sunday 22 November 2026",
    stories: 35,
    regions: 6,
    pictured: 13,
    entry: { file: "entry.png", width, height, bytes: size, sha256 },
    generator: "draw.py (PIL, stdlib-only main.ts)",
  };
}

// --- validate, then copy + dossier (no timestamps: byte-identical runs) ---
const buf = readFileSync(sourcePng);
checkMagic(buf);
const { width, height } = readDimensions(buf);
const size = statSync(sourcePng).size;
checkSize(size);
walkChunks(buf);

mkdirSync(outDir, { recursive: true });
copyFileSync(sourcePng, join(outDir, "entry.png"));
const sha256 = createHash("sha256").update(buf).digest("hex");
const dossier = buildDossier(width, height, size, sha256);
writeFileSync(join(outDir, "dossier.json"), JSON.stringify(dossier, null, 2) + "\n");
console.log(`copied entry.png (${size} bytes, sha256 ${sha256.slice(0, 16)}…)`);
