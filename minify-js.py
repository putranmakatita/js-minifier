# Author: Putra Nurhuda Makatita
# Easy to use minifier
import os
import sys
import subprocess
from pathlib import Path

def minify_file(input_file, output_dir, uglify_path):
    filename = Path(input_file).stem
    output_file = output_dir / f"{filename}.min.js"

    print(f"Sedang meminify '{input_file}'...")
    try:
        subprocess.run([
            uglify_path,
            input_file,
            "-o",
            str(output_file),
            "--compress",
            "--mangle"
        ], check=True)

        if output_file.exists() and output_file.stat().st_size > 0:
            print(f"Sukses: {output_file}")
        else:
            print(f"File hasil kosong untuk: {output_file}. Cek konfigurasi uglifyjs.")
    except subprocess.CalledProcessError:
        print(f"Gagal meminify: {input_file}. Pastikan uglifyjs terinstal dan valid.")

def process_path(input_path, output_dir, uglify_path):
    output_dir.mkdir(exist_ok=True, parents=True)

    if input_path.is_file() and input_path.suffix == ".js":
        minify_file(str(input_path), output_dir, uglify_path)
    elif input_path.is_dir():
        for js_file in input_path.rglob("*.js"):
            minify_file(str(js_file), output_dir, uglify_path)
    else:
        print(f"Path '{input_path}' tidak valid. Berikan file .js atau direktori yang benar.")

def find_uglifyjs():
    print("Mencari path uglifyjs...")
    try:
        result = subprocess.run(["where", "uglifyjs.cmd"], capture_output=True, text=True, check=True)
        uglify_path = result.stdout.strip().split("\n")[0]
        print(f"Menggunakan uglifyjs di: {uglify_path}")
        return uglify_path
    except subprocess.CalledProcessError:
        print("uglifyjs tidak ditemukan di PATH. Install dengan: npm install -g uglify-js")
        sys.exit(1)

def main():
    if len(sys.argv) < 3:
        input_path = input("Masukan path ke file JS-nya atau direktori: ")
        output_dir = input("Masukan path untuk output (default: ./MinJS): ") or "MinJS"
    else:
        input_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) >= 3 else "MinJS"

    input_path = Path(input_path)
    output_dir = Path(output_dir)

    if not input_path.exists():
        print(f"Path '{input_path}' tidak ditemukan. Periksa kembali.")
        sys.exit(1)

    uglify_path = find_uglifyjs()
    print(f"Sedang memproses '{input_path}'...")
    process_path(input_path, output_dir, uglify_path)
    print("Semua proses selesai.")

if __name__ == "__main__":
    main()
