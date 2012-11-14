# When updating the binary version, do not forget to also update baselibs.conf
%define pango_binary_version 1.8.0

Name:           pango
Version:        1.32.1
Release:        2.3
License:        LGPL-2.1+
Summary:        Library for Layout and Rendering of Text
Url:            http://www.pango.org/
Group:          System/Libraries
Source:         http://download.gnome.org/sources/pango/1.32/%{name}-%{version}.tar.xz
Source2:        macros.pango
Source99:       baselibs.conf
BuildRequires:  gcc-c++
BuildRequires:  gtk-doc
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(glib-2.0) >= 2.33.12
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(harfbuzz) >= 0.9.3
BuildRequires:  pkgconfig(libthai) >= 0.1.9
BuildRequires:  pkgconfig(xft) >= 2.0.0
BuildRequires:  pkgconfig(xrender)

%description
Pango is a library for layout and rendering of text, with an emphasis
on internationalization. It can be used anywhere that text layout
is needed.

Pango forms the core of text and font handling for GTK+.

%package -n libpango
Summary:        Library for Layout and Rendering of Text
Group:          System/Libraries
Provides:       %{name} = %{version}
Obsoletes:      %{name} < %{version}
Requires(post): %{name}-tools

%description -n libpango
Pango is a library for layout and rendering of text, with an emphasis
on internationalization. It can be used anywhere that text layout
is needed.

Pango forms the core of text and font handling for GTK+.

%package -n typelib-1_0-Pango-1_0
Summary:        Library for Layout and Rendering of Text -- Introspection bindings
Group:          System/Libraries

%description -n typelib-1_0-Pango-1_0
Pango is a library for layout and rendering of text, with an emphasis
on internationalization. It can be used anywhere that text layout
is needed.

Pango forms the core of text and font handling for GTK+.

This package provides the GObject Introspection bindings for Pango.

%package tools
Summary:        Library for Layout and Rendering of Text -- Tools
Group:          System/Libraries

%description tools
Pango is a library for layout and rendering of text, with an emphasis
on internationalization. It can be used anywhere that text layout
is needed.

Pango forms the core of text and font handling for GTK+.

%package module-thai-lang
Summary:        Library for Layout and Rendering of Text -- Module for the Thai Language
Group:          System/Libraries
Provides:       locale(pango:th_TH)
Requires(post): %{name}-tools
Requires(postun): %{name}-tools

%description module-thai-lang
Pango is a library for layout and rendering of text, with an emphasis
on internationalization. It can be used anywhere that text layout
is needed.

Pango forms the core of text and font handling for GTK+.

%package devel
Summary:        Library for Layout and Rendering of Text -- Development Files
Group:          Development/Libraries/GNOME
Requires:       libpango = %{version}
Requires:       typelib-1_0-Pango-1_0 = %{version}

%description devel
Pango is a library for layout and rendering of text, with an emphasis
on internationalization. It can be used anywhere that text layout
is needed.

Pango forms the core of text and font handling for GTK+.

This package contains all necessary include files and libraries needed
to develop applications that require these.

%prep
%setup -q

%build
%configure --disable-static --with-pic
make %{?_smp_mflags}

%install
%make_install
mkdir -p %{buildroot}%{_sysconfdir}/pango/
touch %{buildroot}%{_libdir}/pango/%{pango_binary_version}/pango.modules
%if "%{_lib}" == "lib64"
mv %{buildroot}%{_bindir}/pango-querymodules %{buildroot}%{_bindir}/pango-querymodules-64
%endif
# Install rpm macros
mkdir -p %{buildroot}%{_sysconfdir}/rpm
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/rpm
# Convenient %%define for the scriplets
%if "%{_lib}" == "lib64"
%define _pango_querymodules %{_bindir}/pango-querymodules-64
%else
%define _pango_querymodules %{_bindir}/pango-querymodules
%endif
%define _pango_querymodules_update_cache %{_pango_querymodules} --update-cache

%post -n libpango
/sbin/ldconfig
%if 0
# In case libpango gets installed before pango-tools, we don't want to
# fail. So we make the call to pango-querymodules dependent on the
# existence of the binary. This is why we also have a %%post for
# pango-tools.
%endif
if test -f %{_pango_querymodules}; then
  %{_pango_querymodules_update_cache}
fi

%if 0
# No need to call pango-querymodules in postun:
# - if it's an upgrade, it will have been called in post
# - if it's an uninstall, we don't care about this anymore
%endif

%postun -n libpango -p /sbin/ldconfig

%post module-thai-lang
%{_pango_querymodules_update_cache}

%postun module-thai-lang
%{_pango_querymodules_update_cache}

%post tools
%if 0
# If we install pango-tools for the first time, then we should run it in case
# libpango was installed first (ie, if
# %%{_libdir}/pango/%%{pango_binary_version} already exists) which means
# pango-querymodules couldn't run there.
%endif
if [ $1 == 1 ]; then
  test -d %{_libdir}/pango/%{pango_binary_version}
  if test $? -eq 0; then
    %{_pango_querymodules_update_cache}
  fi
fi

%files -n libpango
%defattr(-,root,root)
%doc COPYING
%dir %{_libdir}/pango
%dir %{_libdir}/pango/%{pango_binary_version}
%ghost %{_libdir}/pango/%{pango_binary_version}/pango.modules
%dir %{_libdir}/pango/%{pango_binary_version}/modules
%{_libdir}/pango/%{pango_binary_version}/modules/pango-arabic-lang.so
%{_libdir}/pango/%{pango_binary_version}/modules/pango-basic-fc.so
%{_libdir}/pango/%{pango_binary_version}/modules/pango-indic-lang.so
%{_libdir}/lib*.so.*
%dir %{_sysconfdir}/pango

%files -n typelib-1_0-Pango-1_0
%defattr(-,root,root)
%{_libdir}/girepository-1.0/Pango-1.0.typelib
%{_libdir}/girepository-1.0/PangoCairo-1.0.typelib
%{_libdir}/girepository-1.0/PangoFT2-1.0.typelib
%{_libdir}/girepository-1.0/PangoXft-1.0.typelib

%files tools
%defattr(-, root, root)
%{_bindir}/pango-querymodules*
%{_bindir}/pango-view
%doc %{_mandir}/man1/pango-querymodules.1*
%doc %{_mandir}/man1/pango-view.1*

# We have this module in a subpackage because it requires additional libraries.

%files module-thai-lang
%defattr(-, root, root)
%{_libdir}/pango/%{pango_binary_version}/modules/pango-thai-lang.so

%files devel
%defattr(-, root, root)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/pango-1.0/
%{_datadir}/gir-1.0/*.gir
%doc %{_datadir}/gtk-doc/html/pango/
%{_sysconfdir}/rpm/macros.pango
