# Building

Run ./build-docker.sh

Uses docker and poetry to build, and produces firmware blobs for both
bitcoin-only builds and for all enabled currencies.

# Ristretto Support

Added a subset of patches (removed the cmake build system patches and the
separate tests directory) from https://github.com/isislovecruft/ristretto-donna

Checking for symbols in build/core/firmware.bin via:

    nm -an build/core/firmware.elf

# Misc

Uses https://github.com/trezor/blockbook https://wiki.trezor.io/Blockbook to
offload scanning for client transactions via public addresses.  For Monero, the
recommended way is to run a local monero daemon which the wallet talks to,
presumedly for anonymity reasons.
