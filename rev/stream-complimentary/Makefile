.PHONY: build clean

build:
	wasm-pack build --release --target web --out-dir ../site/pkg wasm-flow-free
	rm site/pkg/package.json site/pkg/README.md site/pkg/.gitignore

clean:
	cargo clean --manifest-path ./wasm-flow-free/Cargo.toml