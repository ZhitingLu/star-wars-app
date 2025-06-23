import HeroPage from "@/components/HeroPage";
import PeopleTable from "@/components/PeopleTable";
import PlanetsTable from "@/components/PlanetsTable";

export default function Home() {
  return (
   <>
    <HeroPage />
    <main className="bg-black text-white px-6 py-12">
        <section id="people" className="my-20">
          <h2 className="text-3xl font-bold mb-6">People</h2>
          <PeopleTable />
        </section>

        <section id="planets" className="my-20">
          <h2 className="text-3xl font-bold mb-6">Planets</h2>
          <PlanetsTable />
        </section>
      </main>
   </>
  );
}
