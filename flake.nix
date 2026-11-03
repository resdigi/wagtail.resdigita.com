{
  description = "wagtail.resdigita.com — Wagtail/Django development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f system);
    in
    {
      devShells = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python311;
        in
        {
          default = pkgs.mkShell {
            # venvShellHook provisions .venv and runs the "postVenvCreation"
            # hook the first time it is created.
            venvDir = ".venv";

            # Prefer prebuilt wheels; only fall back to source builds when a
            # compatible wheel is genuinely unavailable for this platform.
            PIP_PREFER_BINARY = 1;
            PIP_NO_CACHE_DIR = 1;
            # Deterministic builds (Nix sets this), avoids build-time issues in
            # some Rust/C backends.
            SOURCE_DATE_EPOCH = 315532800; # 1980-01-01

            buildInputs = [
              python
              python.pkgs.venvShellHook
              # Native build dependencies for compiled Python extensions
              # (pillow_heif, greenlet, lxml-based packages, etc.).
              pkgs.gcc
              pkgs.pkg-config
              pkgs.zlib
              pkgs.libjpeg
              pkgs.libwebp
              pkgs.libtiff
              pkgs.freetype
              pkgs.libheif
              pkgs.openssl
              pkgs.libffi
              # Build toolchain for Rust-based wheels (jiter, orjson, tiktoken,
              # ormsgpack, pydantic_core) and for pillow_heif (cmake).
              pkgs.rustc
              pkgs.cargo
              pkgs.maturin
              pkgs.cmake
              pkgs.ninja
              pkgs.autoconf
              pkgs.automake
              pkgs.libtool
              # Translations (make makemessages / compilemessages).
              pkgs.gettext
              # Tailwind (npm/npx) used by resdigita/tailwind and blog/tailwind.
              pkgs.nodejs_22
              pkgs.gnumake
              pkgs.sqlite
            ];

            postVenvCreation = ''
              .venv/bin/pip install --upgrade pip
              .venv/bin/pip install -r requirements.txt
              (cd resdigita && ../.venv/bin/pip install -r requirements.txt)
            '';

            postShellHook = ''
              export PATH="$PWD/.venv/bin:$PATH"
            '';
          };
        });
    };
}
