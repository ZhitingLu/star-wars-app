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
    <main className="bg-black/70 text-white px-6 py-8">
        <section id="people" className="my-20">
          <h2 className="text-3xl font-bold mb-6 text-center">People</h2>
          <PeopleTable />
        </section>

        <section id="planets" className="my-20">
          <h2 className="text-3xl font-bold mb-6 text-center">Planets</h2>
          <PlanetsTable />
        </section>
      </main>
   </div>
  );
}
