%undefine _debugsource_packages

Name:           tldr
Version:        3.4.4
Release:        2
Summary:        Simplified and community-driven man pages
# sphinx-argparse is not built for Python 3.15, so the man page is not generated
%bcond man 0
Group:          Documentation

License:        MIT
URL:            https://github.com/tldr-pages/tldr-python-client
Source0:        https://github.com/tldr-pages/tldr-python-client/archive/%{version}/%{name}-python-client-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  pkgconfig(python3)
BuildRequires:  python%{pyver}dist(pip)
BuildRequires:  python%{pyver}dist(wheel)
BuildRequires:  python%{pyver}dist(termcolor)
BuildRequires:  python%{pyver}dist(colorama)
BuildRequires:  python%{pyver}dist(shtab)
BuildRequires:  python%{pyver}dist(hatchling)
%if %{with man}
BuildRequires:  make
BuildRequires:  python%{pyver}dist(sphinx)
BuildRequires:  python%{pyver}dist(sphinx-argparse)
%endif
# dependencies for %%check
#BuildRequires:  python3dist(pytest)

Requires: python%{pyver}dist(shtab)

%description
A Python command line client for tldr - Simplified and community-driven
man pages http://tldr-pages.github.io/.

%prep
%autosetup -n tldr-python-client-%{version}
#sed -i 's/>=1\.3\.10//g' requirements.txt

%build
%if %{with man}
pushd docs
make man
popd
%endif
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
# The wheel already installs the man page.
%{_mandir}/man1/tldr.1*
%{python3_sitelib}/__pycache__/tldr.cpython-*.pyc
%{python3_sitelib}/tldr-%{version}.dist-info
%{python3_sitelib}/tldr.py
