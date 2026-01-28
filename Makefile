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
