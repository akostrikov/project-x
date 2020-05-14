#/usr/bin/env sh
curl --data "@tests/fixtures/input.json" -H "Content-Type: application/json" -X POST http://localhost:5000/trip