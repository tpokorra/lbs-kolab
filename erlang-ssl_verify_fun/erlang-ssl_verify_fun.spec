%define bname ssl_verify_fun
Name:           erlang-%bname
Version:        1.1.1
Release:        1
Summary:        SSL verification for Erlang
License:        MIT
Group:          Development/Tools/Other
URL:            https://github.com/deadtrickster/%bname.erl
Source:         %bname.erl-%version.tar.gz

BuildRequires:  erlang-rpm-macros
BuildRequires:  erlang-rebar
BuildRequires:  erlang-erl_interface erlang-public_key

%description
SSL verification for Erlang.


%prep
%setup -q -n %bname.erl-%version

%build
rebar compile -vv
rebar doc -vv

%install
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/ebin
install -p -m 0644 ebin/* %buildroot%_otplibdir/%bname-%version/ebin/
install -d -m 0755 %buildroot%_otplibdir/%bname-%version/doc
install -p -m 0644 doc/*.{css,html,png} %buildroot%_otplibdir/%bname-%version/doc/
install -d -m 0755 %buildroot%_docdir/%name
ln -sf %_otplibdir/%bname-%version/doc %buildroot%_docdir/%name/html
install -p -m 0644 *.md %buildroot%_docdir/%name/

%check
rebar eunit -vv || :

%files
%defattr(-,root,root)
%doc %_docdir/%name
%_otplibdir/*

%changelog
* Sun Nov  6 2016 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> 1.1.1-1
- Initial package
