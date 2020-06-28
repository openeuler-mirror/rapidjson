%global debug_package   %{nil}
Name:                 rapidjson
Version:              1.1.0
Release:              9
Summary:              small & selft-contained fast JSON parser and generator for C++
License:              MIT
URL:                  http://miloyip.github.io/rapidjson
Source0:              https://github.com/miloyip/rapidjson/archive/v%{version}.tar.gz#/rapidjson-%{version}.tar.gz
Patch0000:            rapidjson-1.1.0-do_not_include_gtest_src_dir.patch
BuildRequires:        cmake gcc-c++ gtest-devel valgrind

%description
RapidJSON as a fast JSON parser which generator for c++. It`s inspired by
RapidXML. It`s supports both SAX & DOM style API. It`s small but complete.
It`s fast, It`s preformance can be comparabel to strlen(). It`s self-contained.
It doesn`t depend on external libraries such as BOOST. It`s Unicode and
memory friendly, each JSON valude occupies exactly 16/20 bytes for most
32/64-bit machines. It`s suport UTF-8 UTF-16 UTF-32 (LE & BE).

%package devel
Summary:              small & selft-contained fast JSON parser and generator for C++
BuildArch:            noarch
Provides:             rapidjson = %{version}-%{release}
Provides:             rapidjson-static = %{version}-%{release}
%description devel
RapidJSON as a fast JSON parser which generator for c++. It`s inspired by
RapidXML. It`s supports both SAX & DOM style API. It`s small but complete.
It`s fast, It`s preformance can be comparabel to strlen(). It`s self-contained.
It doesn`t depend on external libraries such as BOOST. It`s Unicode and
memory friendly, each JSON valude occupies exactly 16/20 bytes for most
32/64-bit machines. It`s suport UTF-8 UTF-16 UTF-32 (LE & BE).

%package help
Summary:              Documentation-files for rapidjson
BuildArch:            noarch
BuildRequires:        hardlink doxygen
Provides:             rapidjson-doc = %{version}-%{release}
Obsoletes:            rapidjson-doc < %{version}-%{release}
%description help
This package provides docs for rapidjson.

%prep
%autosetup -n rapidjson-%{version} -p1
install -d build
for _file in "license.txt" $(%{_bindir}/find example -type f -name '*.c*')
do
  %{__sed} -e 's!\r$!!g' < ${_file} > ${_file}.new && \
  /bin/touch -r ${_file} ${_file}.new && \
  %{__mv} -f ${_file}.new ${_file}
done
%{__cp} -a example examples
%{_bindir}/find . -type f -name 'CMakeLists.txt' -print0 | \
 %{_bindir}/xargs -0 %{__sed} -i -e's![ \t]*-march=native!!g' -e's![ \t]*-Werror!!g'

%build
cd build
%cmake -DDOC_INSTALL_DIR=%{_pkgdocdir} -DGTESTSRC_FOUND=TRUE -DGTEST_SOURCE_DIR=. ..
%make_build
cd -

%install
cd build
%make_install
cd -
%{__mv} -f %{buildroot}%{_libdir}/* %{buildroot}%{_datadir}
%{__cp} -a CHANGELOG.md readme*.md examples %{buildroot}%{_pkgdocdir}
%{_bindir}/find %{buildroot} -type f -name 'CMake*.txt' -print0 | \
 %{_bindir}/xargs -0 %{__rm} -fv
%{_sbindir}/hardlink -v %{buildroot}%{_includedir}
%{_sbindir}/hardlink -v %{buildroot}%{_pkgdocdir}

%check
CTEST_EXCLUDE=".*valgrind.*"
cd build
%{_bindir}/ctest -E "${CTEST_EXCLUDE}" -V .
cd -

%files devel
%license license.txt
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/{CHANGELOG.md,readme*.md}
%{_datadir}/cmake
%{_datadir}/pkgconfig/*
%{_includedir}/rapidjson

%files help
%license %{_datadir}/licenses/rapidjson*
%doc %{_pkgdocdir}

%changelog
* Mon Jun 8 2020 Jeffery.Gao <gaojianxing@huawei.com> - 1.1.0-9
- Package init
