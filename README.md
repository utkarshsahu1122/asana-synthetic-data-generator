# Asana Synthetic Data Generator

This repository contains a synthetic data generator that simulates an Asana-like workspace
with realistic users, teams, projects, tasks, subtasks, comments, tags, and custom fields.

The goal is to generate relationally consistent, temporally realistic data suitable for:
- Analytics experimentation
- ML / data science prototyping
- Query and dashboard validation

## Features
- SQLite-backed relational schema
- Realistic task hierarchies and completion behavior
- Time-aware generation (sprints, deadlines, completion lag)
- LLM-assisted text generation for names and descriptions
- Configurable scale (users, projects, tasks)

## Project Structure
- `src/` – core generator logic
- `prompts/` – LLM prompt templates
- `data/` – generated SQLite database
- `docs/` – schema and methodology documentation

## How to Run (WIP)
```bash
python src/main.py
