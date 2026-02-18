.PHONY: install test lint run clean

install:
	npm install

test:
	npx vitest run

lint:
	npx eslint js/

run:
	npm run dev

clean:
	rm -rf node_modules package-lock.json
.PHONY: squash-69

# Recoge los últimos 69 commits y los prepara para un commit maestro
squash-69:
	@echo "📡 Iniciando recolección de 69 commits..."
	git reset --soft HEAD~69
	@echo "📦 Commits extraídos. Listos para re-empaquetar."
	git add .
	git commit -m "💎 CONSOLIDACIÓN MAESTRA: 69 Commits integrados en Divineo v7"
	@echo "✅ Historial simplificado y optimizado."
