# KUBERA Unified Agent Workflow

## Русский

### Роли
- **ChatGPT** — главный исполнитель кода: берёт Issue, создаёт ветку и PR, фиксирует проверки.
- **Claude** — независимый проверяющий: review PR, проверка фактов, работа с ПК, почтой и Google Drive в пределах выданных прав.
- **Copilot** — подсказки внутри GitHub; не является автором PR в этом процессе.
- **Grok** — сводки и черновики писем; ничего не отправляет без решения человека.
- **Nikola** — ставит задачи и единственный, кто выполняет Merge.

### Цикл
`Issue → ветка → PR с "Closes #N" → GitHub Actions → review → Merge`

### Главное правило
Никакой агент не сливает PR и не удаляет файлы без явного «да» Nikola.

## English

### Roles
- **ChatGPT** — primary coding executor: takes an Issue, creates a branch and PR, and records verification.
- **Claude** — independent reviewer: PR review, fact checking, and authorised work with the PC, email and Google Drive.
- **Copilot** — in-GitHub assistance; it is not the PR author in this workflow.
- **Grok** — summaries and email drafts; it does not send messages without human decision.
- **Nikola** — creates/assigns tasks and is the only person who merges PRs.

### Cycle
`Issue → branch → PR with "Closes #N" → GitHub Actions → review → Merge`

### Core rule
No agent merges a PR or deletes files without Nikola's explicit approval.
