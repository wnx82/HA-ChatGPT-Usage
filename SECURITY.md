# SECURITY

## Gestion des secrets

- Ne jamais logger la cle API OpenAI.
- Ne jamais demander ni stocker de mot de passe ChatGPT.
- Ne jamais stocker de cookie ou session token ChatGPT non chiffre.
- Utiliser le mecanisme Home Assistant config entry pour la cle API.
- Masquer les secrets dans `diagnostics.py`.
- Le companion web local doit utiliser un profil navigateur local ignore par Git, jamais un export manuel de cookies ou tokens.

## Fichiers `.env`

- `.env.example` doit rester sans valeur sensible.
- Les fichiers `.env`, `.env.local`, `.env.production` et `.env.staging` sont ignores par defaut.
- Si un `.env` reel doit etre ajoute volontairement dans un depot prive, inspecter chaque variable avant `git add -f .env`.
- Ne jamais copier de secret dans `README.md`, `CHANGELOG.md`, `PROJECT_LOG.md`, `TODO.md` ou `DEPLOYMENT.md`.

## Rotation des cles

1. Creer une nouvelle cle OpenAI admin.
2. Mettre a jour la config entry Home Assistant.
3. Redemarrer ou recharger l'integration.
4. Verifier les capteurs.
5. Revoquer l'ancienne cle.

## Nettoyage d'historique Git

```bash
pip install git-filter-repo
git-filter-repo --sensitive-data-removal --invert-paths --path .env
```

Pour plusieurs fichiers :

```bash
git-filter-repo --sensitive-data-removal --invert-paths --path .env --path .env.local --path .env.production
```

Apres verification :

```bash
git push --force --mirror origin
```

Apres suppression de secrets, prevenir les collaborateurs, verifier les forks, faire re-cloner si necessaire, faire une rotation complete des secrets et verifier que les anciens secrets ne fonctionnent plus.

## Avant passage public

- Supprimer les vrais fichiers `.env`.
- Nettoyer l'historique Git.
- Faire une rotation complete des cles.
- Verifier toute la documentation.
- Verifier les anciens commits.
- Confirmer que `.env.example` ne contient aucune vraie valeur.

## Actions sensibles a eviter

- Logs contenant tokens, cookies, cles API ou mots de passe.
- Ajout automatique de tous les fichiers `.env*`.
- Actions destructives sans confirmation explicite.
- Commit du dossier `.codex-web-companion/` ou de tout profil navigateur local.
