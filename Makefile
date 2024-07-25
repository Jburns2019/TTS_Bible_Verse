.DEFAULT_GOAL := build_website
main_page := index.html
functionality := say_text.py
css := page_style.css
js := scripts.js

#For John.
build_website:
	git add ${main_page}
	git add ${css} ${js}
	git add ${functionality}
	git commit -m "Update website."
	git pull
	git push