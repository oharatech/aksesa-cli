#!/usr/bin/env bash
set -euo pipefail

# Aksesa CLI Installer
# Usage: curl -L ai.codecircle.space/install.sh | bash

REPO="oharatech/aksesa-cli"
BINARY_NAME="aksesa"
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/bin}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    exit 1
}

detect_platform() {
    local os
    local arch

    os=$(uname -s | tr '[:upper:]' '[:lower:]')
    arch=$(uname -m)

    case "$os" in
        linux)
            os="unknown-linux-gnu"
            ;;
        darwin)
            os="apple-darwin"
            ;;
        *)
            error "Unsupported OS: $os"
            ;;
    esac

    case "$arch" in
        x86_64|amd64)
            arch="x86_64"
            ;;
        arm64|aarch64)
            arch="aarch64"
            ;;
        *)
            error "Unsupported architecture: $arch"
            ;;
    esac

    echo "${arch}-${os}"
}

get_latest_tag() {
    local tag
    tag=$(curl -sL "https://api.github.com/repos/${REPO}/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
    if [ -z "$tag" ]; then
        error "Failed to get latest release tag"
    fi
    echo "$tag"
}

main() {
    info "Installing Aksesa CLI..."

    local platform
    platform=$(detect_platform)
    info "Detected platform: $platform"

    local tag
    tag=$(get_latest_tag)
    info "Latest version: $tag"

    local archive_name="${BINARY_NAME}-${tag}-${platform}.tar.gz"
    local download_url="https://github.com/${REPO}/releases/download/${tag}/${archive_name}"
    local tmp_dir
    tmp_dir=$(mktemp -d)
    local archive_path="${tmp_dir}/${archive_name}"

    info "Downloading ${archive_name}..."
    if ! curl -fsL -o "$archive_path" "$download_url"; then
        error "Failed to download ${download_url}"
    fi

    info "Extracting..."
    tar -xzf "$archive_path" -C "$tmp_dir"

    # Create install dir if needed
    if [ ! -d "$INSTALL_DIR" ]; then
        info "Creating install directory: ${INSTALL_DIR}"
        mkdir -p "$INSTALL_DIR"
    fi

    local binary_path="${tmp_dir}/${BINARY_NAME}"
    if [ ! -f "$binary_path" ]; then
        error "Expected binary not found after extraction: ${binary_path}"
    fi

    info "Installing to ${INSTALL_DIR}/${BINARY_NAME}..."
    cp "$binary_path" "${INSTALL_DIR}/${BINARY_NAME}"
    chmod +x "${INSTALL_DIR}/${BINARY_NAME}"

    # Cleanup
    rm -rf "$tmp_dir"

    # Verify
    if command -v "$BINARY_NAME" >/dev/null 2>&1; then
        info "Aksesa CLI installed successfully!"
        info "Version: $(${BINARY_NAME} --version)"
    else
        warn "Aksesa CLI installed to ${INSTALL_DIR}/${BINARY_NAME}, but it is not on your PATH."
        warn "Add the following to your shell profile:"
        echo "    export PATH=\"${INSTALL_DIR}:\$PATH\""
    fi
}

main "$@"
