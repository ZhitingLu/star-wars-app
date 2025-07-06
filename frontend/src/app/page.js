import About from "@/components/About";
import Footer from "@/components/Footer";
import HeroPage from "@/components/HeroPage";
import PeopleTable from "@/components/PeopleTable";
import PlanetsTable from "@/components/PlanetsTable";

export default function Home() {
  return (
    <div className="min-h-screen relative text-white">
      {/* Background video behind everything */}
      <video
        autoPlay
        loop
        muted
        playsInline
        className="fixed inset-0 z-[-1] w-full h-full object-cover"
      >
        <source src="/stars.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <HeroPage />
      <main className="bg-black/70 text-white px-0 sm:px-6  py-8">
        <section id="people" className="my-10">
          <h2
            className="text-3xl font-bold mb-6 text-center
            "
          >
            People
          </h2>
          <PeopleTable />
        </section>

        <section id="planets" className="my-10">
          <h2 className="text-3xl font-bold mb-6 text-center gradient-shadow-text">
            Planets
          </h2>
          <PlanetsTable />
        </section>

        <section id="about" className="my-10">
          <h2 className="text-3xl font-bold mb-6 text-center gradient-shadow-text">
            About
          </h2>
          <About />
        </section>
      </main>
      <Footer />
    </div>
  );
}
