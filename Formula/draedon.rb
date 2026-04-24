class Draedon < Formula
  include Language::Python::Virtualenv

  desc "Modular passive reconnaissance framework"
  homepage "https://github.com/Hybabybabyba/draedon"
  url "https://github.com/Hybabybabyba/draedon/archive/refs/tags/v1.1.0.tar.gz"
  sha256 "" # run: brew fetch --force draedon && brew audit draedon
  license "MIT"
  head "https://github.com/Hybabybabyba/draedon.git", branch: "main"

  depends_on "python@3.12"

  # Auto-generate resource blocks after publishing a release:
  #   brew update-python-resources Formula/draedon.rb
  resource "certifi" do
    url "https://files.pythonhosted.org/packages/source/c/certifi/certifi-2024.8.30.tar.gz"
    sha256 "bec941d2aa8195e248a60b31ff9f0558284cf01a52591ceda73ea9afffd69fd9"
  end

  resource "charset-normalizer" do
    url "https://files.pythonhosted.org/packages/source/c/charset-normalizer/charset-normalizer-3.3.2.tar.gz"
    sha256 "f30c3cb33b24454a82faecaf01b19c18562b1e89558929e8af7df0d95f7cba8a"
  end

  resource "idna" do
    url "https://files.pythonhosted.org/packages/source/i/idna/idna-3.7.tar.gz"
    sha256 "028ff3aadf0609c1fd278d272d50472d1e0073862c1237dd42c7e86f2c8b3b5e"
  end

  resource "urllib3" do
    url "https://files.pythonhosted.org/packages/source/u/urllib3/urllib3-2.2.3.tar.gz"
    sha256 "e7d814a81dad81e6caf2ec9fdedb284ecc9c73076b62654547cc64ccdcae26e9"
  end

  resource "requests" do
    url "https://files.pythonhosted.org/packages/source/r/requests/requests-2.32.3.tar.gz"
    sha256 "55365417734eb18255590a9f9c9c6ce397e05b472e748cec4f18b51e7bf8d65f"
  end

  resource "markdown-it-py" do
    url "https://files.pythonhosted.org/packages/source/m/markdown-it-py/markdown-it-py-3.0.0.tar.gz"
    sha256 "e3f60a94fa066dc52ec76661e37c851cb232d92f9886b15cb560aakulele5f68"
  end

  resource "mdurl" do
    url "https://files.pythonhosted.org/packages/source/m/mdurl/mdurl-0.1.2.tar.gz"
    sha256 "bb413d29f5eea38f31dd4754dd7377d4465116fb207585f97bf925588687c1ba"
  end

  resource "pygments" do
    url "https://files.pythonhosted.org/packages/source/p/pygments/pygments-2.18.0.tar.gz"
    sha256 "786ff802f32e91311bff3889f6e9a86e81505fe99f2735bb6d60ae0c5004f199"
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/source/r/rich/rich-13.9.4.tar.gz"
    sha256 "439594978a49a09530cff7ebc4b5c7103ef57baf48d5ea3184f21d9a2befa098"
  end

  resource "wcwidth" do
    url "https://files.pythonhosted.org/packages/source/w/wcwidth/wcwidth-0.2.13.tar.gz"
    sha256 "3da69048e4540d84af32131829ff948f1e022c1c6bdb8d6102117aac784f6859"
  end

  resource "readchar" do
    url "https://files.pythonhosted.org/packages/source/r/readchar/readchar-4.2.0.tar.gz"
    sha256 "c075d0579bbdb72e8e11c2cc9b5b2048de9a8a5e50e8db6b4f5fe7523a3a2e3"
  end

  resource "blessed" do
    url "https://files.pythonhosted.org/packages/source/b/blessed/blessed-1.20.0.tar.gz"
    sha256 "2cdd67f8746e048f00df47a2880f4d6acbcdb399031a7e047f9c4a27e1a8e53f"
  end

  resource "inquirer" do
    url "https://files.pythonhosted.org/packages/source/i/inquirer/inquirer-3.4.0.tar.gz"
    sha256 "17ef57a880c5e69fbaef72cf2a76cd5f97af3889b18b6cab85ab3a00b4910b4c"
  end

  resource "python-whois" do
    url "https://files.pythonhosted.org/packages/source/p/python-whois/python-whois-0.9.4.tar.gz"
    sha256 "dbc8a485e72b89a6c9d0d14a24d2fea29a4a66d2de47d39a19c7fc843e44ef2f"
  end

  resource "dnspython" do
    url "https://files.pythonhosted.org/packages/source/d/dnspython/dnspython-2.7.0.tar.gz"
    sha256 "ce9c432eda0dc91cf618a5cedf1a4bf386d3c9f38a6d5573c53a0f9eeacfe1fb"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "module", shell_output("#{bin}/draedon --list 2>&1")
  end
end
