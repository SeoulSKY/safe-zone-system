FROM jboss/keycloak:15.0.2

COPY safe-zone-realm.json /tmp/safe-zone-realm.json
ENV KEYCLOAK_IMPORT /tmp/safe-zone-realm.json
ENV KEYCLOAK_MIGRATION_STRATEGY OVERWRITE_EXISTING
