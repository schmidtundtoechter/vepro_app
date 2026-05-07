### vepro_app

Diese App wurde für VEPRO geschrieben. 
Sie dienst als Ergänzung zu ERPNext 15 und soll alle UI Veränderungen am System beinhalten. 

Die drei wichtigsten Branches sind: 
main:      Hier findet man den komplett durchgetesteten und funktionierenden Code.
staging:   Code der durch SUT getestet wurde. Es muss noch durch VEPPRO selbst zur Migration in den Main-Branch freigegeben werden.
develop:   Code im Zwischenstadium befindet sich hier oder im passenden Feature Branch.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app vepro_app
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/vepro_app
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
