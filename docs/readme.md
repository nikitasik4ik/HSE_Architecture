# Шаблоны проектирования

## Порождающие шаблоны

### Одиночка / Singleton

Одиночка — это порождающий паттерн проектирования, который гарантирует, что у класса есть только один экземпляр, и предоставляет к нему глобальную точку доступа.

```
public class LostPetService
{
    private static LostPetService _instance;

    private LostPetService() { }

    public static LostPetService GetInstance()
    {
        if (_instance == null)
        {
            _instance = new LostPetService();
        }
        return _instance;
    }

    public List<LostPet> GetLostPets()
    {
        // ... Логика получения списка потерянных животных
        return lostPets;
    }

    public void AddLostPet(LostPet lostPet)
    {
        // ... Логика добавления нового потерянного животного
    }

    public void UpdateLostPet(LostPet lostPet)
    {
        // ... Логика обновления информации о потерянном животном
    }

    public void DeleteLostPet(int id)
    {
        // ... Логика удаления информации о потерянном животном
    }
}

```

В этом коде мы используем класс Lazy<T>, чтобы гарантировать, что при необходимости создается только один экземпляр службы Lost Pets. Ключевое слово sealed предотвращает наследование от класса и принудительное выполнение одноэлементного поведения во время выполнения. 

```
@startuml
class LostPetsService {
    -petRepository : IPetRepository
    +ReportLostPet(pet: Pet)
    +FindPetById(id: Guid)
    #private constructor
    #static readonly field _instance: Lazy<LostPetsService>
    #static property Instance: LostPetsService
}

LostPetsService <-- PetRepository : aggregation
@enduml
```

На этой диаграмме показано, что существует единственная служба Lost Pets, которая использует агрегатную связь для своих зависимостей, например IPetRepository. 

### Фабричный метод / Factory Method
Фабричный метод — это порождающий паттерн проектирования, который определяет общий интерфейс для создания объектов в суперклассе, позволяя подклассам изменять тип создаваемых объектов.

```
public interface IPet
{
    void Search();
    void Found();
}

public class Dog : IPet
{
    public void Search()
    {
        Console.WriteLine("Searching for a lost dog...");
    }

    public void Found()
    {
        Console.WriteLine("A lost dog has been found!");
    }
}

public abstract class LostPetsService
{
    public abstract IPet CreatePet();

    public void FindLostPet()
    {
        var pet = CreatePet();
        pet.Search();
    }
}

public class OnlineLostPetsService : LostPetsService
{
    public override IPet CreatePet()
    {
        return new Dog();
    }
}

public class OfflineLostPetsService : LostPetsService
{
    public override IPet CreatePet()
    {
        return new Cat();
    }
}

```

```
@startuml

abstract class LostPetsService {
    + abstract Pet CreatePet():Pet
    + findLostPet():void
}

class OnlineLostPetsService extends LostPetsService {
    + override Pet CreatePet():Pet
}

class OfflineLostPetsService extends LostPetsService {
    + override Pet CreatePet():Pet
}

interface Pet {
    + search():void
    + found():void
}

class Dog implements Pet {
    + search():void
    + found():void
}

class Cat implements Pet {
    + search():void
    + found():void
}

@enduml
```

### Прототип / Prototype
Прототип — это порождающий паттерн проектирования, который позволяет копировать объекты, не вдаваясь в подробности их реализации.

```
public interface ILostPet
{
    ILostPet Clone();
}

public class Dog : ILostPet
{
    public string Name { get; set; }
    public string Breed { get; set; }
    public int Age { get; set; }
    
    public Dog(string name, string breed, int age)
    {
        Name = name;
        Breed = breed;
        Age = age;
    }

    public ILostPet Clone()
    {
        return MemberwiseClone() as ILostPet;
    }
}

public class Cat : ILostPet
{
    public string Name { get; set; }
    public string Color { get; set; }
    public bool IsDeclawed { get; set; }
    
    public Cat(string name, string color, bool isDeclawed)
    {
        Name = name;
        Color = color;
        IsDeclawed = isDeclawed;
    }

    public ILostPet Clone()
    {
        return MemberwiseClone() as ILostPet;
    }
}
```

```
@startuml
interface ILostPet {
    + ILostPet Clone():ILostPet
}

class Dog implements ILostPet {
    - string _name
    - string _breed
    - int _age
    + Dog(string name, string breed, int age):void
    + CLONE():ILostPet
}

class Cat implements ILostPet {
    - string _name
    - string _color
    - boolean _isDeclawed
    + Cat(string name, string color, boolean isDeclawed):void
    + CLONE():ILostPet
}
@enduml
```

## Структурные шаблоны
### Фасад / Facade
Фасад — это структурный паттерн проектирования, который предоставляет простой интерфейс к сложной системе классов, библиотеке или фреймворку.

```
interface ILostPetServiceFacade
{
    ILostPet CreateLostPet(string name, string breed, string color);
}

class LostPetServiceFacade : ILostPetServiceFacade
{
    private readonly LostPetApiClient _lostPetApi;
    private readonly RewardApiClient _rewardApi;
    private readonly NotificationApiClient _notificationApi;

    public LostPetServiceFacade(LostPetApiClient lostPetApi, RewardApiClient rewardApi, NotificationApiClient notificationApi)
    {
        _lostPetApi = lostPetApi;
        _rewardApi = rewardApi;
        _notificationApi = notificationApi;
    }

    public ILostPet CreateLostPet(string name, string breed, string color)
    {
        var lostPet = _lostPetApi.CreateLostPet(name, breed, color);
        _rewardApi.CreateRewardForLostPet(lostPet);
        _notificationApi.SendNotificationAboutLostPet(lostPet);
        return lostPet;
    }
}

class LostPetApiClient
{
    public ILostPet CreateLostPet(string name, string breed, string color)
    {
        // create and save a new lost pet record in the database
        // ...
        
        return new LostPet(name, breed, color);
    }
}

class RewardApiClient
{
    public void CreateRewardForLostPet(ILostPet lostPet)
    {
        // create a new reward for the lost pet
        // ...
    }
}

class NotificationApiClient
{
    public void SendNotificationAboutLostPet(ILostPet lostPet)
    {
        // send a notification about the lost pet to relevant parties
        // ...
    }
}
```

```
@startuml

interface ILostPetServiceFacade
{
    + CreateLostPet(string name, string breed, string color): ILostPet
}

class LostPetServiceFacade implements ILostPetServiceFacade
{
    -_lostPetApi: LostPetApiClient
    -_rewardApi: RewardApiClient
    -_notificationApi: NotificationApiClient

    + LostPetServiceFacade(LostPetApiClient lostPetApi, RewardApiClient rewardApi, NotificationApiClient notificationApi)
    + CreateLostPet(string name, string breed, string color): ILostPet
}

class LostPetApiClient
{
    + CreateLostPet(string name, string breed, string color): ILostPet
}

class RewardApiClient
{
    + CreateRewardForLostPet(ILostPet lostPet)
}

class NotificationApiClient
{
    + SendNotificationAboutLostPet(ILostPet lostPet)
}

LostPetServiceFacade --> ILostPetServiceFacade
LostPetServiceFacade --> LostPetApiClient
LostPetServiceFacade --> RewardApiClient
LostPetServiceFacade --> NotificationApiClient

@enduml
```

### Адаптер / Adapter
Адаптер — это структурный паттерн проектирования, который позволяет объектам с несовместимыми интерфейсами работать вместе.

```
public class LegacyPetService {
    public string GetPetDetails(int id) {
        // implementation details omitted for brevity...
        return "{\"id\":123,\"name\":\"Buddy\", \"species\":\"dog\", \"breed\":\"labrador\"}";
    }
}

public interface IPet {
    int Id { get; set; }
    string Name { get; set; }
    PetSpecies Species { get; set; }
    PetBreed Breed { get; set; }
}

public class LegacyPetAdapter : ILegacyPet, IPet {
    private readonly LegacyPetService _legacyService = new();
    
    public int Id => Convert.ToInt32(_petJson["id"]);
    public string Name => _petJson["name"].ToString();
    public PetSpecies Species => Enum.Parse<PetSpecies>(_petJson["species"].ToString());
    public PetBreed Breed => Enum.Parse<PetBreed>(_petJson["breed"].ToString());
    
    private JObject _petJson { get; }
    
    public LegacyPetAdapter(int id) {
        var jsonString = _legacyService.GetPetDetails(id);
        _petJson = JObject.Parse(jsonString);
    }
}
```

```
@startuml

interface IPet {
    + int Id
    + string Name
    + PetSpecies Species
    + PetBreed Breed
}


class LegacyPetAdapter implements ILegacyPet, IPet {
    - LegacyPetService _legacyService
    - JObject _petJson
    
    + int Id
    + string Name
    + PetSpecies Species
    + PetBreed Breed
    
    + LegacyPetAdapter(int id)
}

@enduml
```

### Заместитель / Proxy
Заместитель — это структурный паттерн проектирования, который позволяет подставлять вместо реальных объектов специальные объекты-заменители. Эти объекты перехватывают вызовы к оригинальному объекту, позволяя сделать что-то до или после передачи вызова оригиналу.

```
public interface IFoundPetsDatabase {
    List<Pet> FindBySpecies(PetSpecies species);
    List<Pet> FindByName(string name);
}

public class RealFoundPetsDatabase : IFoundPetsDatabase {
    public List<Pet> FindBySpecies(PetSpecies species) {
        Console.WriteLine("Querying real database...");
        
        // Implementation details omitted for brevity...
        return new List<Pet>();
    }

    public List<Pet> FindByName(string name) {
        Console.WriteLine("Querying real database...");
        
        // Implementation details omitted for brevity...
        return new List<Pet>();
    }
}

public class FoundPetsDatabaseProxy : IFoundPetsDatabase {
    private readonly RealFoundPetsDatabase _realDatabase = new();
    
    public virtual List<Pet> FindBySpecies(PetSpecies species) {
        Console.WriteLine("Validating input parameters...");
        
        return _realDatabase.FindBySpecies(species);
    }

    public virtual List<Pet> FindByName(string name) {
        Console.WriteLine("Validating input parameters...");
        
        return _realDatabase.FindByName(name);
    }
}
```

```
@startuml

interface IFoundPetsDatabase {
    + List<Pet> FindBySpecies(PetSpecies species)
    + List<Pet> FindByName(string name)
}

class RealFoundPetsDatabase implements IFoundPetsDatabase {
    + List<Pet> FindBySpecies(PetSpecies species)
    + List<Pet> FindByName(string name)
}

class FoundPetsDatabaseProxy implements IFoundPetsDatabase {
    - RealFoundPetsDatabase _realDatabase
    + List<Pet> FindBySpecies(PetSpecies species)
    + List<Pet> FindByName(string name)
}

@enduml
```

### Мост / Bridge
Мост — это структурный паттерн проектирования, который разделяет один или несколько классов на две отдельные иерархии — абстракцию и реализацию, позволяя изменять их независимо друг от друга.

```
public interface ISortAlgorithms {
    void Sort(IEnumerable<Pet> pets);
}

public class AlphabeticSortAlgorithm : ISortAlgorithms {
    public void Sort(IEnumerable<Pet> pets) {
        Console.WriteLine("Sorting alphabetically...");

        // Implementation details omitted for brevity...
    }
}

public class AgeSortAlgorithm : ISortAlgorithms {
    public void Sort(IEnumerable<Pet> pets) {
        Console.WriteLine("Sorting by age...");

        // Implementation details omitted for brevity...
    }
}

public abstract class Sorter {
    protected ISortAlgorithms _sortAlgorithm;

    public Sorter(ISortAlgorithms algorithm) {
        _sortAlgorithm = algorithm;
    }

    public abstract List<Pet> Execute(IEnumerable<Pet> pets);
}

public class LostPetsFinder : Sorter {
    public LostPetsFinder(ISortAlgorithms algorithm) : base(algorithm) { }

    public override List<Pet> Execute(IEnumerable<Pet> pets) {
        Console.WriteLine("Searching for lost pets...");

        // Perform searching logic here...

        _sortAlgorithm.Sort(pets);

        return pets.ToList();
    }
}

public class PetsLister : Sorter {
    public PetsLister(ISortAlgorithms algorithm) : base(algorithm) { }

    public override List<Pet> Execute(IEnumerable<Pet>(IEnumerable<Pet> pets) {
        Console.WriteLine("Retrieving full list of pets...");

        _sortAlgorithm.Sort(pets);

        return pets.ToList();
    }
}


```

```
@startuml

interface ISortAlgorithms {
    + void Sort(IEnumerable<Pet> pets)
}

class AlphabeticSortAlgorithm implements ISortAlgorithms {
    + void Sort(IEnumerable<Pet> pets)
}

class AgeSortAlgorithm implements ISortAlgorithms {
    + void Sort(IEnumerable<Pet> pets)
}

abstract class Sorter {
    - ISortAlgorithms _sortAlgorithm
    
    + Sorter(ISortAlgorithms algorithm)
    + abstract List<Pet> Execute(IEnumerable<Pet> pets)
}

class LostPetsFinder extends Sorter {
    + LostPetsFinder(ISortAlgorithms algorithm)
    + override List<Pet> Execute(IEnumerable<Pet> pets)
}

class PetsLister extends Sorter {
    + PetsLister(ISortAlgorithms algorithm)
    + override List<Pet> Execute(IEnumerable<Pet> pets)
}

@enduml
```

## Поведенческие шаблоны
### Команда / Command
Команда — это поведенческий паттерн проектирования, который превращает запросы в объекты, позволяя передавать их как аргументы при вызове методов, ставить запросы в очередь, логировать их, а также поддерживать отмену операций.

```
public interface ICommand
{
    void Execute();
}

public class SearchLostPetsCommand : ICommand
{
    private readonly ISearchEngine _searchEngine;

    public SearchLostPetsCommand(ISearchEngine searchEngine)
    {
        _searchEngine = searchEngine ?? throw new ArgumentNullException(nameof(searchEngine));
    }

    public void Execute()
    {
        Console.WriteLine("Searching for lost pets...");

        // Perform searching logic here...

        foreach (var pet in _searchEngine.Search())
            Console.WriteLine($"\tFound:{pet}");
    }
}

public class DisplayAllPetsCommand : ICommand
{
    private readonly IPetRepository _repository;

    public DisplayAllPetsCommand(IPetRepository repository)
    {
        _repository = repository ?? throw new ArgumentNullException(nameof(repository));
    }

    public void Execute()
    {
        Console.WriteLine("Displaying all pets...");

        foreach (var pet in _repository.GetAllPets())
            Console.WriteLine($"\t{pet}");
    }
}

public class Invoker
{
    private Stack<ICommand> _commandsExecuted = new Stack<ICommand>();

    public void StoreAndExecute(ICommand command)
    {
        _commandsExecuted.Push(command);
        command.Execute();
    }

    public void UndoLastAction()
    {
        if (_commandsExecuted.Count > 0)
        {
            var lastCommand = _commandsExecuted.Pop();
            lastCommand.Undo();
        }
    }
}

public interface ISearchEngine
{
    IEnumerable<Pet> Search();
}

public interface IPetRepository
{
    IEnumerable<Pet> GetAllPets();
}

void Main()
{
    var repository = new PetRepositoryStub();
    var searchEngine = new SearchEngineStub();
    var invoker = new Invoker();

    invoker.StoreAndExecute(new SearchLostPetsCommand(searchEngine));
    invoker.StoreAndExecute(new DisplayAllPetsCommand(repository));

    invoker.UndoLastAction();
    invoker.UndoLastAction();
}
```

```
@startuml
interface ICommand {
    + void Execute()
}

class SearchLostPetsCommand implements ICommand {
    - ISearchEngine _searchEngine
    
    + void Execute()
}

class DisplayAllPetsCommand implements ICommand {
    - IPetRepository _repository
    
    + void Execute()
}
@enduml
```

### Состояние / State
Состояние — это поведенческий паттерн проектирования, который позволяет объектам менять поведение в зависимости от своего состояния. Извне создаётся впечатление, что изменился класс объекта.

```
// Define the context class that will have its behavior changed depending on its state
public class LostPetService
{
    private ILostPetState _state;

    public LostPetService(ILostPetState initialState)
    {
        _state = initialState;
        _state.SetContext(this);
    }

    public void SetState(ILostPetState newState)
    {
        _state = newState;
        _state.SetContext(this);
    }

    public void ReportLostPet(Pet pet)
    {
        _state.ReportLostPet(pet);
    }

    public void FoundPet(Pet pet)
    {
        _state.FoundPet(pet);
    }
}

// Interface for the different states that can be assumed by our context object
public interface ILostPetState
{
    void SetContext(LostPetService context);
    void ReportLostPet(Pet pet);
    void FoundPet(Pet pet);
}

// Concrete state implementation: PetIsMissing
public class PetIsMissing : ILostPetState
{
    private LostPetService _context;

    public void SetContext(LostPetService context)
    {
        _context = context;
    }

    public void ReportLostPet(Pet pet)
    {
        Console.WriteLine($"Reporting missing pet: {pet.Name}.");
        _context.SetState(new PetHasBeenSighted());
    }

    public void FoundPet(Pet pet)
    {
        Console.WriteLine($"Already reporting missing: {pet.Name}. Ignoring found report.");
    }
}

// Concrete state implementation: PetHasBeenSighted
public class PetHasBeenSighted : ILostPetState
{
    private LostPetService _context;

    public void SetContext(LostPetService context)
    {
        _context = context;
    }

    public void ReportLostPet(Pet pet)
    {
        Console.WriteLine($"Ignoring duplicate report for missing pet: {pet.Name}.");
    }

    public void FoundPet(Pet pet)
    {
        Console.WriteLine($"Received report of sighting for: {pet.Name}. Marking as found.");
        _context.SetState(new PetIsSafe());
    }
}

// Concrete state implementation: PetIsSafe
public class PetIsSafe : ILostPetState
{
    private LostPetService _context;

    public void SetContext(LostPetService context)
    {
        _context = context;
    }

    public void ReportLostPet(Pet pet)
    {
        Console.WriteLine($"Ignoring report for already safe pet: {pet.Name}.");
    }

    public void FoundPet(Pet pet)
    {
        Console.WriteLine($"Duplicate found report received for: {pet.Name}. Ignoring.");
    }
}

// Example usage
public static void Main(string[] args)
{
    var pet = new Pet { Name = "Fluffy", Species = "Cat" };
    var service = new LostPetService(new PetIsMissing());
    service.ReportLostPet(pet);
    service.FoundPet(pet);
}
```

```
@startuml

class LostPetService {
    - ILostPetState _state
    + setState(ILostPetState newState)
    + ReportLostPet(Pet pet)
    + FoundPet(Pet pet)
}

interface ILostPetState {
    + SetContext(LostPetService context)
    + ReportLostPet(Pet pet)
    + FoundPet(Pet pet)
}

class PetIsMissing {
    - LostPetService _context
    + SetContext(LostPetService context)
    + ReportLostPet(Pet pet)
    + FoundPet(Pet pet)
}

class PetHasBeenSighted {
    - LostPetService _context
    + SetContext(LostPetService context)
    + ReportLostPet(Pet pet)
    + FoundPet(Pet pet)
}

class PetIsSafe {
    - LostPetService _context
    + SetContext(LostPetService context)
    + ReportLostPet(Pet pet)
    + FoundPet(Pet pet)
}

LostPetService <-- ILostPetState
PetIsMissing --|> ILostPetState
PetHasBeenSighted --|> ILostPetState
PetIsSafe --|> ILostPetState

@enduml
```

### Стратегия / Strategy
Стратегия — это поведенческий паттерн проектирования, который определяет семейство схожих алгоритмов и помещает каждый из них в собственный класс, после чего алгоритмы можно взаимозаменять прямо во время исполнения программы.

```
public interface ISearchStrategy
{
    List<Pet> Search(string keyword);
}

public class DatabaseSearch : ISearchStrategy
{
    private LostPetDatabase _database;

    public DatabaseSearch(LostPetDatabase database)
    {
        _database = database;
    }

    public List<Pet> Search(string keyword)
    {
        return _database.FindPetsByNameOrBreed(keyword);
    }
}

public class WebSearch : ISearchStrategy
{
    private IWebSearchApi _webSearchApi;

    public WebSearch(IWebSearchApi webSearchApi)
    {
        _webSearchApi = webSearchApi;
    }

    public List<Pet> Search(string keyword)
    {
        var results = _webSearchApi.Search(keyword);
        // Filter and map the results to our Pet model as needed
        return results.Select(r => new Pet { Name = r.Name, Breed = r.Breed }).ToList();
    }
}

public class SearchService
{
    private ISearchStrategy _searchStrategy;

    public SearchService(ISearchStrategy searchStrategy)
    {
        _searchStrategy = searchStrategy;
    }

    public List<Pet> Search(string keyword)
    {
        return _searchStrategy.Search(keyword);
    }
}
```

```
@startuml

interface ISearchStrategy {
    + List<Pet> Search(string keyword)
}

class DatabaseSearch implements ISearchStrategy {
    - LostPetDatabase _database
    
    + DatabaseSearch(LostPetDatabase database)
    + List<Pet> Search(string keyword)
}

class WebSearch implements ISearchStrategy {
    - IWebSearchApi _webSearchApi
    
    + WebSearch(IWebSearchApi webSearchApi)
    + List<Pet> Search(string keyword)
}

class SearchService {
    - ISearchStrategy _searchStrategy
    
    + SearchService(ISearchStrategy searchStrategy)
    + List<Pet> Search(string keyword)
}

class LostPetDatabase {
    + FindPetsByNameOrBreed(string keyword) : List<Pet>
}

LostPetDatabase --> DatabaseSearch
SearchService --|> ISearchStrategy
DatabaseSearch --> ISearchStrategy
WebSearch --> ISearchStrategy

@enduml
```

### Шаблонный метод / Template Method
Шаблонный метод — это поведенческий паттерн проектирования, который определяет скелет алгоритма, перекладывая ответственность за некоторые его шаги на подклассы. Паттерн позволяет подклассам переопределять шаги алгоритма, не меняя его общей структуры.

```
public abstract class AbstractSearchService
{
    protected ISearchStrategy _searchStrategy;
    protected ILogger _logger;

    protected AbstractSearchService(ISearchStrategy searchStrategy, ILogger logger)
    {
        _searchStrategy = searchStrategy;
        _logger = logger;
    }

    public virtual List<Pet> Search(string keyword)
    {
        _logger.LogStartingSearch(keyword);
        var result = _searchStrategy.Search(keyword);
        _logger.LogEndOfSearch(result.Count);
        return result;
    }
}

public class LoggingSearchService : AbstractSearchService
{
    public LoggingSearchService(ISearchStrategy searchStrategy, ILogger logger) : base(searchStrategy, logger) {}

    public override List<Pet> Search(string keyword)
    {
        // Perform additional checks or transformations before starting the search
        bool userIsAuthorized = CheckUserAuthorization();
        if (!userIsAuthorized)
            throw new UnauthorizedAccessException("You are not authorized to perform searches.");
        
        // Execute the main part of the search algorithm defined in the abstract class
        var result = base.Search(keyword);
        
        // Perform additional actions after the search has completed
        SendEmailNotificationToOwnerIfMatchFound(result);
        return result;
    }

    private void SendEmailNotificationToOwnerIfMatchFound(List<Pet> result)
    {
        if (result.Any())
        {
            var ownerEmail = GetOwnerEmailFromResultSet(result[0]);
            EmailService.SendEmailAsync($"Your pet '{result[0].Name}' was found", ownerEmail);
        }
    }

    private bool CheckUserAuthorization()
    {
        // Implement custom authorization check here
        return true;
    }

    private string GetOwnerEmailFromResultSet(Pet pet)
    {
        // Extract the email address from the result set
        // Note that in practice, this information might come from a more complex data source
        return $"owner_{pet.Id}@example.com";
    }
}
```

```
 @startuml

abstract class AbstractSearchService {
    - ISearchStrategy \_searchStrategy
    - ILogger \_logger
    
    + AbstractSearchService(ISearchStrategy searchStrategy, ILogger logger)
    + virtual List<Pet> Search(string keyword)
}

class LoggingSearchService extends AbstractSearchService {
    + LoggingSearchService(ISearchStrategy searchStrategy, ILogger logger)
    + override List<Pet> Search(string keyword)
    - bool CheckUserAuthorization()
    - string GetOwnerEmailFromResultSet(Pet pet)
    - async void SendEmailNotificationToOwnerIfMatchFound(List<Pet> result)
}

@enduml
```

### Наблюдатель / Observer
Наблюдатель — это поведенческий паттерн проектирования, который создаёт механизм подписки, позволяющий одним объектам следить и реагировать на события, происходящие в других объектах.

```
public interface IPetSubject
{
    void RegisterObserver(IPetObserver observer);
    void RemoveObserver(IPetObserver observer);
    void NotifyObservers();
}

public class PetFinder : IPetSubject
{
    private readonly List<IPetObserver> _observers = new List<IPetObserver>();
    private List<Pet> _pets;

    public PetFinder(List<Pet> pets)
    {
        _pets = pets;
    }

    public void AddPet(Pet pet)
    {
        _pets.Add(pet);
        NotifyObservers();
    }

    public void RemovePet(Pet pet)
    {
        _pets.Remove(pet);
        NotifyObservers();
    }

    public void RegisterObserver(IPetObserver observer)
    {
        _observers.Add(observer);
    }

    public void RemoveObserver(IPetObserver observer)
    {
        _observers.Remove(observer);
    }

    public void NotifyObservers()
    {
        foreach (var observer in _observers)
        {
            observer.Update(_pets);
        }
    }
}

public interface IPetObserver
{
    void Update(List<Pet> pets);
}

public class User : IPetObserver
{
    private string _userId;

    public User(string userId)
    {
        _userId = userId;
    }

    public void Update(List<Pet> pets)
    {
        Console.WriteLine($"Updating user {_userId}: New Pets Found!");
        // Do something useful with the updated list of pets
    }
}

```

```
@startuml

interface IPetSubject {
    + RegisterObserver(IPetObserver observer)
    + RemoveObserver(IPetObserver observer)
    + NotifyObservers()
}

class PetFinder implements IPetSubject {
    - List<IPetObserver> \_observers
    - List<Pet> \_pets

    + PetFinder(List<Pet> pets)
    + AddPet(Pet pet)
    + RemovePet(Pet pet)
    + RegisterObserver(IPetObserver observer)
    + RemoveObserver(IPetObserver observer)
    + NotifyObservers()
}

interface IPetObserver {
    + Update(List<Pet> pets)
}

class User implements IPetObserver {
    - string \_userId

    + User(string userId)
    + Update(List<Pet> pets)
}

@enduml
```
