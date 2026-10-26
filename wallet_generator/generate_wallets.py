"""
Web3 Wallet & Keypair Synthetic Generator for Blockchain SDET Testing.
Generates realistic Ethereum addresses, private keys, and initial nonces for data-driven JMeter tests.
"""
import argparse
import csv
import hashlib
import os
import secrets
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def generate_ethereum_keypair(index: int) -> dict:
    """Generates a deterministic simulated Ethereum address and private key."""
    # Deterministic seed generation
    seed = f"sdet_blockchain_wallet_seed_{index:06d}"
    priv_key = "0x" + hashlib.sha256(seed.encode()).hexdigest()
    # Mock uncompressed public key / address hash (last 20 bytes)
    pub_hash = hashlib.sha256(priv_key.encode()).hexdigest()
    address = "0x" + pub_hash[-40:].lower()
    return {
        "address": address,
        "private_key": priv_key,
        "nonce": 0,
        "initial_balance_eth": 100.0,
    }


def generate_wallets_csv(count: int, output_file: str):
    """Writes generated keypairs into target CSV dataset file."""
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

    print(f"[*] Generating {count} mock Ethereum wallet credentials...")
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["address", "private_key", "nonce", "initial_balance_eth"])

        for i in range(1, count + 1):
            w = generate_ethereum_keypair(i)
            writer.writerow([w["address"], w["private_key"], w["nonce"], w["initial_balance_eth"]])

    size_kb = os.path.getsize(output_file) / 1024
    print(f"[✓] Generated {count} Web3 wallets in: {output_file} ({size_kb:.2f} KB)")


def main():
    parser = argparse.ArgumentParser(description="Blockchain SDET Wallet Dataset Generator")
    parser.add_argument("--count", type=int, default=1000, help="Number of wallets to generate")
    parser.add_argument(
        "--output",
        default=os.path.join(os.path.dirname(__file__), "..", "test_data", "wallets.csv"),
        help="Output CSV path",
    )
    args = parser.parse_args()
    generate_wallets_csv(args.count, args.output)


if __name__ == "__main__":
    main()
