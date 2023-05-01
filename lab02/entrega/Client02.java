import java.rmi.Naming;
import java.util.ArrayList;
import java.util.Scanner;

public class Client02 {
	private Scanner in; 
	private ICinema cinema;
	
	public Client02() {
		in = new Scanner(System.in);
		if(System.getSecurityManager() == null) {
			System.setSecurityManager(new SecurityManager());
		}	    	 
		try {  
			cinema =(ICinema)Naming.lookup( "rmi://127.0.0.1/Cinema");  
		}
		catch(Exception e ) {  
			System.out.println();  
			System.out.println("Exception: " + e.toString());  
		}
	}
	
	public void execute() {
		String comando;
		int key;
		
		try {
            while(true) {
                System.out.println("\nEscolha uma das opções a seguir:\n 1. Reservar uma cadeira\n 2. Consultar uma cadeira\n 3. Consultar número total de cadeiras\n 4. Sair");
				comando = in.next();
				if (comando.equalsIgnoreCase("1")) {
                    System.out.println("Digite o número da cadeira a ser reservada:");
					key = in.nextInt();
					if (cinema.reservar(key)) System.out.println("Reservou a cadeira " + key);
                    else System.out.println("Cadeira " + key + " indisponível");
				} else if(comando.equalsIgnoreCase("2")) {
                    System.out.println("Digite o número da cadeira a ser consultada:");
                    key = in.nextInt();
					System.out.println("A cadeira " + key + " está " + ((consultarCadeira(cinema.consultar(), key)) ? "disponível" : "indisponível"));
				} else if(comando.equalsIgnoreCase("3")) {
					System.out.println("Número total de cadeiras (disponíveis e indisponíveis): " + cinema.consultar().size());
				} else if (comando.equalsIgnoreCase("4")) {
					System.out.println("Saindo do programa");
					break;
				}
			}
		    in.close();
		}catch(Exception e) {		
			System.out.println("Exception: " + e.toString());
		}
	}

    private Boolean consultarCadeira(ArrayList<Boolean> cadeiras, int cadeira) {
        cadeira--;
        if (cadeira < 0 || cadeira >= cadeiras.size()) return false;
        else return cadeiras.get(cadeira);
    }
	
	public static void main(String[] args) {
		Client02 c = new Client02();
		c.execute();
	}

}
