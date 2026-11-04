# F6-R6 validation procedure

The review validator is read-only with respect to experimental evidence and never invokes Syft or CMake:

```sh
python3 scripts/validate_f6_r6.py . --cff-schema /path/to/cff-1.2.0-schema.json
sha256sum -c SHA256SUMS-PUBLIC
```

The exact CFF schema URL and SHA-256 are recorded in `validation/f6-r6/citation-validation.json`. Run the first command from outside the candidate or replace `.` with the candidate path.

The final physical package validation and archive SHA-256 are detached beside the candidate directory to avoid a self-referential manifest. `SHA256SUMS-PUBLIC` covers every regular file in the directory except itself.

These checks validate package integrity and the documented invariants. They do not perform external experimental reproduction.

