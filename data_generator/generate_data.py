"""
Test Data Generator for SDET Performance Testing.
Generates realistic CSV user datasets for JMeter parameterized load testing.
"""
import argparse
import csv
import os
import random
import sys


def generate_users(count: int, output_file: str):
    """Generates a CSV file containing user credentials for JMeter."""
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

    roles = ["customer", "vip_customer", "wholesale"]
    passwords = ["SecretPass123!", "PerfLoad2026#", "SecureUser99$"]

    print(f"[*] Generating {count} performance test users into: {output_file}")

    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Header for JMeter CSV Data Set Config
        writer.writerow(["username", "password", "role", "email"])

        for i in range(1, count + 1):
            username = f"user_perf_{i:05d}"
            password = random.choice(passwords)
            role = random.choice(roles)
            email = f"{username}@perf-test.internal"
            writer.writerow([username, password, role, email])

    file_size_kb = os.path.getsize(output_file) / 1024
    print(f"[✓] Successfully generated {count} records ({file_size_kb:.2f} KB).")


def main():
    parser = argparse.ArgumentParser(description="SDET Performance Test Data Generator")
    parser.add_argument(
        "--count",
        type=int,
        default=1000,
        help="Number of user records to generate (default: 1000)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "..", "test_data", "users.csv"),
        help="Target output CSV file path",
    )
    args = parser.parse_args()

    generate_users(args.count, args.output)


if __name__ == "__main__":
    main()
