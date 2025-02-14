%undefine _debugsource_packages

Name:           tldr
Version:        3.3.0
Release:        1
Summary:        Simplified and community-driven man pages

License:        MIT
URL:            https://github.com/tldr-pages/tldr-python-client
Source0:        https://github.com/tldr-pages/tldr-python-client/archive/%{version}/%{name}-python-client-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  pkgconfig(python)
# dependencies for make man
BuildRequires:  make
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(termcolor)
BuildRequires:  python3dist(colorama)
BuildRequires:  python3dist(shtab)
BuildRequires:  python3dist(sphinx-argparse)
# dependencies for %%check
#BuildRequires:  python3dist(pytest)

Requires: python3.11dist(shtab)

%description
A Python command line client for tldr - Simplified and community-driven
man pages http://tldr-pages.github.io/.

%prep
%autosetup -n %{name}-python-client-%{version}
sed -i 's/>=1\.3\.10//g' requirements.txt

%build
pushd docs
make man
popd
%py_build
#{python3} tldr.py --print-completion bash > tldr.bash
#{python3} tldr.py --print-completion zsh > tldr.zsh

%install
%py_install
#pyproject_install
#pyproject_save_files tldr

#install -Dp --mode=0644 %{name}.bash %{buildroot}%{bash_completions_dir}/%{name}
#install -Dp --mode=0644 %{name}.zsh  %{buildroot}%{zsh_completions_dir}/_%{name}

#check
#pytest -k "not test_error_message"

%files
%license LICENSE.md
%doc CHANGELOG.md README.md
%{_bindir}/%{name}
%{_mandir}/man1/tldr.1*
#{bash_completions_dir}/%{name}
#{zsh_completions_dir}/_%{name}
%{python3_sitelib}/__pycache__/tldr.cpython-*.pyc
%{python3_sitelib}/tldr-%{version}.dist-info
%{python3_sitelib}/tldr.py
