# Divercité AI Agent — INF8175 Project (Winter 2025)

This project is developed as part of the **INF8175 - Artificial Intelligence** course at Polytechnique Montréal. The objective is to design and implement an intelligent agent capable of playing the strategic board game **Divercité** autonomously and competitively.

## 🧩 Project Summary

**Divercité** is a two-player board game where players take turns placing either cities or colored resources on a shared grid. The goal is to strategically surround one’s cities with resource tiles to maximize points based on two main scoring rules:

- **Diversity Bonus**: 5 points for cities surrounded by four differently colored resources.
- **Similarity Bonus**: 1–4 points depending on the number of surrounding resources that match the city’s color.

## 🎯 Project Objective

The primary goal is to implement an AI agent that can:
- Analyze the game board dynamically.
- Make optimal decisions under time constraints.
- Adapt its strategy based on the current game state and potential opponent moves.

## ⚙️ Key Features

- Implemented in **Python 3.11+**
- Agent logic built around a custom decision-making strategy (e.g., heuristic evaluation, Minimax, or MCTS)
- Strict **15-minute time budget** for all moves
- Designed to work with the **Abyss** platform for online agent competition and evaluation
- Lightweight and memory-efficient to comply with platform constraints

## 🏆 Evaluation

The project is assessed on:
- Performance of the agent against baseline and competitive opponents
- Clarity and quality of the strategic design

## 📄 Deliverables

- `my_player.py` – Main agent implementation
- `requirements.txt` – List of required dependencies
- Report (max 5 pages) – Describing the agent’s logic, results, and insights

## 🧠 Learning Goals

- Apply AI decision-making techniques in a real-time, adversarial environment
- Translate game rules into formalized strategies
- Balance algorithmic efficiency with intelligent behavior under resource limits

---

Designed with strategy. Built with intelligence.

