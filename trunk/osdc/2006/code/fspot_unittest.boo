import NUnit.Framework from "nunit.framework"
import LibGPhoto2 from "libgphoto2-sharp.dll"

[TestFixture]
class LibGPhoto2Fixture:
    [Test]
    def TestCamera():
        assert Camera()

    [Test]
    def Testcontext():
        assert Context()
