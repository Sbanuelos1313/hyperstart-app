services:
  - type: web
    name: hyperstart
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: hyperstart-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: ANTHROPIC_API_KEY
        sync: false

databases:
  - name: hyperstart-db
    databaseName: hyperstart
    user: hyperstart
