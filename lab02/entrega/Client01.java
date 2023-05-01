import java.rmi.Naming;
import java.util.ArrayList;
import java.util.Scanner;

public class Client01 {
	private Scanner in; 
	private ICinema cinema;
	
	public Client01() {
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
			System.out.println("Entre com um dos comandos a seguir:\n \t\treservar <int cadeira>\n\t\tconsultar\n\t\tsair");
			while(true) {
				comando = in.next();
				if(comando.equalsIgnoreCase("reservar")) {
					key = in.nextInt();
					if (cinema.reservar(key)) System.out.println("Reservou a cadeira " + key);
                    else System.out.println("Cadeira " + key + " indisponível");
				} else if(comando.equalsIgnoreCase("consultar")) {
					System.out.println(cadeirasDisponiveis(cinema.consultar()));
				} else if (comando.equalsIgnoreCase("sair")) {
					System.out.println("Saindo do programa");
					break;
				}
			}
		    in.close();
		}catch(Exception e) {		
			System.out.println("Exception: " + e.toString());
		}
	}

	private String cadeirasDisponiveis(ArrayList<Boolean> cadeiras) {
		String strCadeiras = "Cadeiras disponíveis:\n";
		for (int i = 0; i < cadeiras.size(); i++) {
			if (cadeiras.get(i)) {
				if (i+1 < 10)
					strCadeiras += "0";
				strCadeiras += Integer.toString(i+1) + " ";
			} else {
				strCadeiras += "   ";
			}
			if ((i+1) % 10 == 0)
				strCadeiras += "     "; 
			if ((i+1) % 30 == 0)
				strCadeiras += "\n";
		}
		return strCadeiras;
	}
	
	public static void main(String[] args) {
		Client01 c = new Client01();
		c.execute();
	}

}
