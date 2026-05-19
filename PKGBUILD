# Maintainer: Soumadip Das <soumadip@zohomail.in>
pkgname=quikrun
pkgver=0.1.0
pkgrel=1
pkgdesc="Run your code without hassle"
arch=("any")
url="https://github.com/soymadip/quikrun"
license=("GPL3")
depends=("python")
makedepends=("python-build" "python-installer" "python-wheel" "python-uv-build")
source=("$pkgname-$pkgver.tar.gz::https://github.com/soymadip/quikrun/releases/download/v$pkgver/$pkgname-$pkgver.tar.gz")
sha256sums=("SKIP")

build() {
    cd "$srcdir/$pkgname-$pkgver" || exit 1
    python -m build --wheel --no-isolation
}

package() {
    cd "$srcdir/$pkgname-$pkgver" || exit 1
    python -m installer --destdir="$pkgdir" dist/*.whl
}
