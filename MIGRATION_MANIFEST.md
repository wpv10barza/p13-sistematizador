# MIGRATION_MANIFEST

- source: Google Drive
- source_folder: `Proyectos_Exportados/SistematizadorEntrevistas`
- project_family: `P13`
- version: `v29` (según README del proyecto)
- github_repository: `wpv10barza/p13-sistematizador`
- github_branch: `import/drive-2026-09-29-v29`
- verified_source_commit: `7bce777c5d196a384dcb73184ba11beecf78b031`
- files_expected: 14 archivos fuente principales + README/configuración segura/CI/manifest
- files_migrated: 14 archivos fuente principales; los bytes coinciden con el snapshot de Drive salvo `config.py`, modificado de forma deliberada y documentada por seguridad/portabilidad.
- files_excluded: `db_config.json*`, `edge_selenium_profile/`, `.git/`, `__pycache__/`, `data/`, `inputs/`, `outputs/`, archivos vacíos de argumentos CLI
- security_changes: `config.py` sustituye dos rutas locales corporativas por variables de entorno/fallbacks locales; `db_config.json` se reemplaza por `db_config.example.json` sin secretos.
- github_tree: `450adfb17f9eb7ad289ba824d7e4f241caf21396`
- ci_workflow_run: `36581854319`
- ci_job: `syntax`
- ci_result: `success`
- verification_status: `CI_PASSED_PRE_MERGE`
- verified_at: `2026-09-29T14:20:02Z`
- deletion_allowed: `false` (la familia P13 conserva variantes históricas y archivos sensibles/no versionables en Drive)

## SHA-256 de archivos fuente en Drive

- `main.py`: `2a9b1ee7b97fcf28c447e6dd4bf3381a3e6d8cc4e1fa9b1e7a462a80f50ba1e2`
- `config.py`: `06af1cccc64b67b3b2cf013496932bc68d58c94b3026b57a29c14d4a7cb9f850`
- `requirements.txt`: `aa2add9ad651ea20681bf969ffcf7572fc473864c526609709efa977724975ad`
- `db.py`: `52ef119b25b5ea5dcea7411854b4da710a6b81a5248f2b79fc81315595d6fa20`
- `db_questions.py`: `840e732e2913514f3602c248ad56415b682c8018cfebaea4001c776fecab4cc0`
- `excel_reader.py`: `d002bdc5cb68cd15b893821076ad104b5824499bca50d1f9e4aab7538257d0d5`
- `exporter.py`: `c9f8f760030ff8b0d44c251895f4ed850161e14942fab3a5f77fcacc4a9bce8b`
- `loaders.py`: `15ec420cb1ad105c0460a0cf81fff13e81b0a198b6e3a0c858a8647c7b147747`
- `mapping.py`: `29678ce09ff7285aa02500af1bc991dee65277921da6fdad12d2193af3fbff83`
- `merge_runner.py`: `f683434698f6d1de8bc5437d6ac1bd594a469dde978764e3e75769fdd207791a`
- `prompt_builder.py`: `bf5ed15d6575303d0a218bac9bdd96d8a4668617003162dd84c59ff3b0af861e`
- `repo.py`: `d15c7687debae134c41da563f717e73ff7847cd18a70ebf403a3066e5b5896d7`
- `selenium_runner.py`: `94040feb0370d29b5c9b0496ab1948ba50adf03f35ff36adb432cbb8a8cf3d16`
- `tsv_utils.py`: `e51e0864dd8c67289acb9b0e1116d1412a0b181cecdfb25d769e76518833233f`
