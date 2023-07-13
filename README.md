# Phasis

A ChatGPT-powered tool to visualize the pulse of and track changes in digital gardens.  
Made in Svelte and Python, October 2022 to April 2023.  
Released under the [MIT License](./LICENSE).  
Created by [Kewbish](https://github.com/kewbish).

## Usage

Phasis is a proof-of-concept — to use:

- `pip install -r requirements.txt`
- change `DIR` in [`phasis.py`](https://github.com/kewbish/phasis/blob/master/phasis.py) to point to the Git repository containing your notes
- get your ChatGPT session token from the cookies, and paste it into `config.json` with the key `session_token`
- update the prompt and maximum comparison length in [`fetch_from_chatgpt`](https://github.com/kewbish/phasis/blob/6c92149f7a40639a6bc481e81f57d503608099cb/phasis.py#L229) in `phasis.py`
- `source venv/bin/activate && cd backend && flask run` to run the Python backend
  - the first time you run this, it'll run a Spacy pipeline to extract all named dates in your notes so it may take a while
- `npm run dev` to run the Svelte frontend; paste the same `DIR` as in `phasis.py`
