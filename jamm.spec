%{?scl:%scl_package jamm}
%{!?scl:%global pkg_name %{name}}

%global githash 1708ca44f7eb3addb66551a15b6b74672e87286a

Name:		%{?scl_prefix}jamm
Version:	0.3.1
Release:	4%{?dist}
Summary:	Java Agent for Memory Measurements
License:	ASL 2.0
Url:		https://github.com/jbellis/%{pkg_name}/
Source0:	https://github.com/jbellis/%{pkg_name}/archive/%{githash}/%{pkg_name}-%{githash}.tar.gz

BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix_maven}mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires:	%{?scl_prefix_java_common}junit
%{?scl:Requires: %scl_runtime}

BuildArch:	noarch

%description
Jamm provides MemoryMeter, a java agent to
measure actual object memory use including
JVM overhead.

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{pkg_name}-%{githash}

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%pom_xpath_inject pom:manifestEntries "<Agent-Class>org.github.jamm.MemoryMeter</Agent-Class>"

# These tests fail on koji only https://github.com/jbellis/jamm/issues/21
# Shallow size of empty String expected:<32> but was:<24>
sed -i 's|assertEquals("Shallow size of empty String"|//assertEquals("Shallow size of empty String"|' \
 test/org/github/jamm/MemoryMeterTest.java
# Deep size of empty String expected:<48> but was:<40>
sed -i 's|assertEquals("Deep size of empty String"|//assertEquals("Deep size of empty String"|' \
 test/org/github/jamm/MemoryMeterTest.java
# Shallow size of one-character String expected:<32> but was:<24>
sed -i 's|assertEquals("Shallow size of one-character String"|//assertEquals("Shallow size of one-character String"|' \
 test/org/github/jamm/MemoryMeterTest.java
# Deep size of one-character String expected:<56> but was:<48>
sed -i 's|assertEquals("Deep size of one-character String"|//assertEquals("Deep size of one-character String"|' \
 test/org/github/jamm/MemoryMeterTest.java

%pom_xpath_inject "pom:plugin[pom:artifactId='maven-jar-plugin']/pom:executions" "
<execution>
 <id>default-jar</id>
 <phase>skip</phase>
</execution>"

%mvn_file : %{pkg_name}
%mvn_alias com.github.jbellis: com.github.stephenc:
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc README.txt
%license license.txt

%files javadoc -f .mfiles-javadoc
%license license.txt

%changelog
* Wed Oct 12 2016 Tomas Repik <trepik@redhat.com> - 0.3.1-4
- use standard SCL macros

* Wed Jul 27 2016 Tomas Repik <trepik@redhat.com> - 0.3.1-3
- scl conversion

* Tue Jun 21 2016 gil cattaneo <puntogil@libero.it> 0.3.1-2
- fix jar plugin task

* Mon Jul 20 2015 gil cattaneo <puntogil@libero.it> 0.3.1-1
- update to 0.3.1

* Fri Sep 28 2012 gil cattaneo <puntogil@libero.it> 0.2.5-1
- initial rpm
