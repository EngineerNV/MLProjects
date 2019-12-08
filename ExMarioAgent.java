/**
 * Copyright John Asmuth and Rutgers University 2009, all rights reserved.
 */


/*
 * Submission for group Nick and Zach;
 * Collaborators are group John and Jeremy.
 */

package edu.rutgers.rl3.comp;

import org.rlcommunity.rlglue.codec.AgentInterface;
import org.rlcommunity.rlglue.codec.types.Action;
import org.rlcommunity.rlglue.codec.types.Observation;
import org.rlcommunity.rlglue.codec.util.AgentLoader;

import java.util.Date;
import java.util.Vector;
import java.util.Random;

// Extra imports from the Vaping Parakeets:
import org.json.*;
import java.io.*;
import java.util.*;
import java.util.Hashtable;
import java.lang.Math.*;

/**
 * A simple agent that:
 * - never goes to the left
 * - mostly goes to the right
 * - tends to jump when under coins
 * - jumps if it cannot walk to the right due to a block
 * - tends to jump when there is a monster nearby
 * - tends to jump when there is a pit nearby
 * - tends to run when there is nothing nearby
 * 
 * Also, it will remember the last trial, and repeat it exactly except
 * for the last 7 steps (assuming there are at least 7 steps).
 * 
 * @author jasmuth, made amazing by Parakeet Vaper 4 lyfe zabuelhaj
 *
 */
public class ExMarioAgent implements AgentInterface {
	// Need to declare the number of states and actions for the policy table:
	private static final int NUMBER_OF_STATES = 13;
	private static final int NUMBER_OF_ACTIONS = 12;
	private static final int MONSTER_NEAR = 0;
	private static final int MONSTER_FAR = 1;
	private static final int MONSTER_ABOVE = 2;
	private static final int MONSTER_BELOW = 3;
	private static final int PIT_FAR = 4;
	private static final int PIT_NEAR = 5;
	private static final int QUESTION_BLOCK = 6;
	private static final int BONUS_ITEM_FAR = 7;
	private static final int BONUS_ITEM_NEAR = 8;
	private static final int COINS = 9;
	private static final int BREAKABLE_BLOCK = 10;
	private static final int HIGHER_GROUND_NEAR = 11;
	private static final int HIGHER_GROUND_FAR = 12;
	private static final int SOFT_POLICY = 4;					// Soft policy for exploration.
	private static final double LEARNING_RATE = 0.069;			// Learning rate for Monte Carlo policy updates.
	private final String filename = "ref_export.json";

	// For the states, actions, and rewards:
	private ArrayList<Integer> state_vector;
	private ArrayList<Integer> action_vector;
	private ArrayList<Double> reward_vector;

	private double[][] policy_table;
	private double[][] reward_table;
	private int[][] iteration_table;
	private double total_reward;
	private double episode_reward;
	private Boolean[] cur_state;

	Map<Integer, Integer> findActionCol;

	/*
	 * Initializes the Policy Table to all zeros:
	 */

	private void initPolicyTable () {
		int rows = (int) Math.pow(2, NUMBER_OF_STATES);
		int cols = NUMBER_OF_ACTIONS;

		policy_table = new double[rows][NUMBER_OF_ACTIONS];
        reward_table = new double[rows][NUMBER_OF_ACTIONS];
        iteration_table = new int[rows][NUMBER_OF_ACTIONS];

        for (int i = 0; i < rows; i++){
            for (int j = 0; j < cols; j++){
                policy_table[i][j] = 0.0;
                reward_table[i][j] = 0.0;
                iteration_table[i][j] = 0;
            }
        }
	}

	/**
	 * Returns the char representing the tile at the given location.
	 * If unknown, returns '\0'.
	 * 
	 * Valid tiles:
	 * M - the tile mario is currently on. there is no tile for a monster.
	 * $ - a coin
	 * b - a smashable brick
	 * ? - a question block
	 * | - a pipe. gets its own tile because often there are pirahna plants
	 *     in them
	 * ! - the finish line
	 * And an integer in [1,7] is a 3 bit binary flag
	 *  first bit is "cannot go through this tile from above"
	 *  second bit is "cannot go through this tile from below"
	 *  third bit is "cannot go through this tile from either side"
	 * 
	 * @param x
	 * @param y
	 * @param obs
	 * @return
	 */
	public static char getTileAt(double xf, double yf, Observation obs) {
		int x = (int)xf;
		if (x<0)
			return '7';
		int y = 16-(int)yf;
		x -= obs.intArray[0];
		if (x<0 || x>21 || y<0 || y>15)
			return '\0';
		int index = y*22+x;
		return obs.charArray[index];
	}
	
	/**
	 * All you need to know about a monster.
	 * 
	 * @author jasmuth
	 *
	 */
	static class Monster {
		double x;
		double y;
		/**
		 * The instantaneous change in x per step
		 */
		double sx;
		/**
		 * The instantaneous change in y per step
		 */
		double sy;
		/**
		 * The monster type
		 * 0 - Mario
		 * 1 - Red Koopa
		 * 2 - Green Koopa
		 * 3 - Goomba
		 * 4 - Spikey
		 * 5 - Pirahna Plant
		 * 6 - Mushroom
		 * 7 - Fire Flower
		 * 8 - Fireball
		 * 9 - Shell
		 * 10 - Big Mario
		 * 11 - Fiery Mario
		 */
		int type;
		/**
		 * A human recognizable title for the monster
		 */
		String typeName;
		/**
		 * Winged monsters bounce up and down
		 */
		boolean winged;
	}
	
	/**
	 * Gets all the monsters from the observation. Mario is included in this list.
	 * 
	 * @param obs
	 * @return
	 */
	public static Monster[] getMonsters(Observation obs) {
		Vector<Monster> monster_vec = new Vector<Monster>();
		for (int i=0; 1+2*i<obs.intArray.length; i++) {
			Monster m = new Monster();
			m.type = obs.intArray[1+2*i];
			m.winged = obs.intArray[2+2*i]!=0;
			switch (m.type) {
			case 0:
				m.typeName = "Mario";
				break;
			case 1:
				m.typeName = "Red Koopa";
				break;
			case 2:
				m.typeName = "Green Koopa";
				break;
			case 3:
				m.typeName = "Goomba";
				break;
			case 4:
				m.typeName = "Spikey";
				break;
			case 5:
				m.typeName = "Piranha Plant";
				break;
			case 6:
				m.typeName = "Mushroom";
				break;
			case 7:
				m.typeName = "Fire Flower";
				break;
			case 8:
				m.typeName = "Fireball";
				break;
			case 9:
				m.typeName = "Shell";
				break;
			case 10:
				m.typeName = "Big Mario";
				break;
			case 11:
				m.typeName = "Fiery Mario";
				break;
			}
			m.x = obs.doubleArray[4*i];
			m.y = obs.doubleArray[4*i+1];
			m.sx = obs.doubleArray[4*i+2];
			m.sy = obs.doubleArray[4*i+3];
			monster_vec.add(m);
		}
		return monster_vec.toArray(new Monster[0]);
	}
	/**
	 * Gets just mario's information.
	 * 
	 * @param obs
	 * @return
	 */
	public static Monster getMario(Observation obs) {
		Monster[] monsters = getMonsters(obs);
		for (Monster m : monsters) {
			if (m.type == 0 || m.type == 10 || m.type == 11)
				return m;
		}
		return null;
	}
	
	Random rand;
	/**
	 * When this is true, Mario is pausing for some number of steps
	 */
	boolean walk_hesitating;
	/**
	 * How many steps since the beginning of this trial
	 */
	int step_number;
	/**
	 * How many steps since the beginning of this run
	 */
	int total_steps;
	/**
	 * The time that the current trial began
	 */
	long trial_start;

	/**
	 * The sequence of actions taken during the last trial
	 */
	Vector<Action> last_actions;
	/**
	 * The sequence of actions taken so far during the current trial
	 */
	Vector<Action> this_actions;

	/*
	 * Switch-case that gets the action from action index:
	 */

	int[] getActionIndex (int act) {
		// First int is the direction (still or move forward/back), second and third are jump and speed (respectively).
		switch (act) {
			case 0:
				return new int[]{-1,0,0};
			case 1:
				return new int[]{-1,0,1};
			case 2:
				return new int[]{-1,1,0};
			case 3:
				return new int[]{-1,1,1};
			case 4:
				return new int[]{0,0,0};
			case 5:
				return new int[]{0,0,1};
			case 6:
				return new int[]{0,1,0};
			case 7:
				return new int[]{0,1,1};
			case 8:
				return new int[]{1,0,0};
			case 9:
				return new int[]{1,0,1};
			case 10:
				return new int[]{1,1,0};
			case 11:
				return new int[]{1,1,1};
			default:
				System.out.println("SOMEHOW A PARAKEET HAS AQCUIRED VAPE\n");
				return new int[]{6,6,6};
		}
	}

	private String getActionString(int act){
	    switch (act){
	        case 0:
	            return "walk back    ";
	        case 1:
	            return "run back     ";
	        case 2:
	            return "jump back    ";
	        case 3:
	            return "big jump back";
	        case 4:
	            return "idle         ";
	        case 5:
	            return "jump in place";
	        case 6:
	            return "idle         ";
	        case 7:
	            return "jump in place";
	        case 8:
	            return "walk forward ";
	        case 9:
	            return "run forward  ";
	        case 10:
	            return "jump forward ";
	        case 11:
	            return "big jump forw";
	        default:
	            return "unknown";

	    }
	}

	/*
	 * Function that prints out an example of what Mario is learning:
	 */

	private void printPolicy(int num){
        System.out.println("Policy table for state " + num + ": ");
        double largest = Double.NEGATIVE_INFINITY;
        int largest_ind = -1;
		for (int i = 0; i < NUMBER_OF_ACTIONS; i++){
		    System.out.println(getActionString(i) + ": " + policy_table[num][i]);
		    if (policy_table[num][i] > largest){
		        largest = policy_table[num][i];
		        largest_ind = i;
		    }
		}
		System.out.println("Largest: " + largest + " | Preferred action: " + getActionString(largest_ind));

	}

	/*
	 * Indenting function that is used in the importing and exporting json functions:
	 */
	
	private String indent(int numOfTabsToAdd){
	    String result = "";
	    for (int i = 0; i < numOfTabsToAdd; i++){
	        result += "\t";
	    }
	    return result;
	}
	

	/*
	 * Returns the index of the policy table when given a current state array:
	 */
	
	int getPolicyIndex (Boolean[] states) {
		String gen_string = "";
		for (boolean s : states) {
			gen_string += s ? "1" : "0";
		}
		return Integer.parseInt(gen_string, 2);
	}

	/*
	 * Converts the direction, jump, and speed integers to a location in the policy table:
	 */

	int getActionCol(int direction, int jump, int speed){
		 int firstDigit = (direction + 1) * 100;
		 int secondDigit = jump * 10;
		 int thirdDigit = speed;
		 return firstDigit + secondDigit + thirdDigit;
	}

	/*
	 * Function to update the policy table.
	 * Uses a radical method provided by Dr. Emma Hayes, master of Machine Learning.
	 * Updated_Reward = Learning_Rate * [Current_Reward - Policy_Reward]:
	 */

	public void updatePolicyTable () {
		int ind1, ind2;
		for (int itr = 0; itr < reward_vector.size(); itr++) {
			ind1 = state_vector.get(itr);
            ind2 = action_vector.get(itr);

            iteration_table[ind1][ind2]++;
            reward_table[ind1][ind2] += episode_reward;

			policy_table[ind1][ind2] = reward_table[ind1][ind2] / (double)(iteration_table[ind1][ind2]);
			episode_reward -= reward_vector.get(itr);
		}
	}
	
	ExMarioAgent() {
		rand = new Random(new java.util.Date().getTime());
		last_actions = new Vector<Action>();
		this_actions = new Vector<Action>();

		// Initialize things that only happen per episode, they get cleared later:
		cur_state = new Boolean[NUMBER_OF_STATES];
		state_vector = new ArrayList<Integer>();
		action_vector = new ArrayList<Integer>();
		reward_vector = new ArrayList<Double>();

		// Initialize the findActionCol hashtable for action lookup:
		findActionCol = new Hashtable<Integer, Integer>();
		int counter = 0;
		for (int dir = -1; dir < 2; dir++){
			 for (int jum = 0; jum < 2; jum++){
				 	for (int spe = 0; spe < 2; spe++){
						findActionCol.put(getActionCol(dir, jum, spe), counter);
						counter++;
					}
			 }
		}

		// Call the initialize Policy Table function here:
		initPolicyTable();

		// Import data from the Json file, if available:
		importPolicy();
	}

	public void agent_init(String task) {
		total_steps = 0;
	}
	
	public void agent_cleanup() {
		System.out.println("THE GAME IS OVER\nTHE PARAKEET (AKA BUDGIE for you English folks) HAS VAPED HIS LAST VAPE\n");
		exportPolicy();
	}
	
	public Action agent_start(Observation o) {
		trial_start = new Date().getTime();
		step_number = 0;

		// Initialize the episode_reward to 0:
		episode_reward = 0;

		// Print out some policy information:
		printPolicy(0);

		return getAction(o);
	}

	public Action agent_step(double r, Observation o) {
		step_number++;
		total_steps++;
		reward_vector.add(r);
		total_reward += r;
		episode_reward += r;

		return getAction(o);
	}

	public void agent_end(double r) {
		// Update the reward variables, reward_vector, and policy_table:
		total_reward += r;
		episode_reward += r;
		reward_vector.add(r);
		updatePolicyTable();

		// Clear the reward, action, and state vectors:
		reward_vector.clear();
		action_vector.clear();
		state_vector.clear();

		long time_passed = new Date().getTime()-trial_start;
		if (this_actions.size() > 7) {
			last_actions = this_actions;
			last_actions.setSize(last_actions.size()-7);
		}
		else
			last_actions = new Vector<Action>();
		this_actions = new Vector<Action>();
		System.out.println("ended after "+total_steps+" total steps");
		System.out.println("average "+1000.0*step_number/time_passed+" steps per second");
	}

	public String agent_message(String msg) {
		return null;
	}

	/*
	 * Get Action for Mario. Uses Monte Carlo Soft Policy with a 25% change that he will explore.
	 * The states are determined by a combination of true/false values in the cur_state array.
	 * There are 2^13 states, due to the cur_state array. 
	 * This function was developed with Jeremy R.
	 */
	
	Action getAction(Observation o) {
		Random rand_ = new Random();
		int exploreProb = rand_.nextInt(SOFT_POLICY);
		
		// Reset remenant state flags:
		for (int i = 0; i < cur_state.length; i ++) {
			cur_state[i] = false;
		}

		// Create a new action array, mario object, and monster object array:
		Action act = new Action(3, 0);
		Monster mario = ExMarioAgent.getMario(o);
		Monster[] monsters = ExMarioAgent.getMonsters(o);

		// Check for the high ground, Anakin!
		for (int i = 0; i < 6; i++) {
			char tile = ExMarioAgent.getTileAt(mario.x+i, mario.y+1, o);
			if (tile != ' ' && tile != 'M' && tile != '\0'){
                if (i < 3){
                    cur_state[HIGHER_GROUND_NEAR] = true;
                } else {
                    cur_state[HIGHER_GROUND_FAR] = true;
                }
                break;
            }
		}

		// Check if there are blocks near the fat plumber in his upper-right:
		for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 7; j++) {
                char tile = ExMarioAgent.getTileAt(mario.x+j, mario.y+i, o);
                if (tile == '?') cur_state[QUESTION_BLOCK] = true;
                if (tile == 'b') cur_state[BREAKABLE_BLOCK] = true;
                if (tile == '$') cur_state[COINS] = true;
            }
        }

        // Check for a pit near meowio:
        boolean is_pit = false;
        boolean pit_col = true;
        int right;
        for (right = 0; !is_pit && right < 6; right++) {
            pit_col = true;
            for (int down = 0; pit_col && mario.y-down >= 0; down++) {
                char tile = ExMarioAgent.getTileAt(mario.x+right, mario.y-down, o);
                if (tile != ' ' && tile != 'M' && tile != '\0')
                    pit_col = false;
            }
            if (pit_col){
                is_pit = true;
            }
        }

        if (is_pit && right < 3) {
            cur_state[PIT_NEAR] = true;
        } else if (is_pit) {
            cur_state[PIT_FAR] = true;
        }

        // Fun Fact: Pacman was going to be called Pucman, but it sounds too much like Fuck Man.
        for (Monster m : monsters) {
            if (m.type == 0 || m.type == 10 || m.type == 11 || m.type == 8) {
                continue;
            }

            double dx = m.x-mario.x;
            double dy = m.y-mario.y;
            if (m.type == 6 || m.type == 7){
                if (dx < -3 && dx > 3){
                    cur_state[BONUS_ITEM_FAR] = true;
                } else {
                    cur_state[BONUS_ITEM_NEAR] = true;
                }
            } else {
                if (dx > -2 && dx < 8)
                    cur_state[MONSTER_NEAR] = true;
                else if (dx > 6 && dx < 15)
                  cur_state[MONSTER_FAR] = true;
                if (dy > 1 && dy < 15 && dx > 0)
                    cur_state[MONSTER_ABOVE] = true;
                else if (dy < -1 && dy > -15 && dx > 0)
                    cur_state[MONSTER_BELOW] = true;
            }
        }

        // Remember the exploreProb variable from the beginning of the function? Well this is him now:
        if (exploreProb != 0) {
			double bv = Double.NEGATIVE_INFINITY;
			int bv_i = 0;
			double val;

			int forLength = policy_table[getPolicyIndex(cur_state)].length;
			for (int i = 0; i < forLength; i++) {
			    val = policy_table[getPolicyIndex(cur_state)][i];

				if (val > bv) {
					bv_i = i;
					bv = policy_table[getPolicyIndex(cur_state)][i];
				}
			}
            int[] cur_action = getActionIndex(bv_i);

            act.intArray = cur_action;

		} else {
			rand_ = new Random();
			act.intArray[0] = rand_.nextInt(3) - 1;
			act.intArray[1] = rand_.nextInt(2);
			act.intArray[2] = rand_.nextInt(2);
		}

		int state_index = getPolicyIndex(cur_state);
		int action_index = findActionCol.get(getActionCol(act.intArray[0], act.intArray[1], act.intArray[2]));
		state_vector.add(state_index);
		action_vector.add(action_index);

		//add the action to the trajectory being recorded, so it can be reused next trial
		this_actions.add(act);

		return act;
	}
	
	private void importPolicy(){
	    Scanner s = null;

        try{
            s = new Scanner(new File(filename));
	    } catch (Exception e){
	        System.out.println("No previous learning to import.");
	        return;
	    }
	    System.out.println("Using previous learning from " + filename + ".");
        System.out.println("Reading from file:");

	    String jsonStr = "";
        s.useDelimiter("\\Z");
        jsonStr += s.next();
	    s.close();
	    System.out.println("Parsing json.");
        JSONObject j_obj = new JSONObject(jsonStr);

        // Read total_reward
        total_reward = j_obj.getDouble("Total Reward");

	    // Read policy_table
	    JSONArray pt_ija = j_obj.getJSONArray("Policy Table");
	    for (int i = 0; i < pt_ija.length(); i++){
	        JSONArray pt_jja = pt_ija.getJSONArray(i);
	        for (int j = 0; j < pt_jja.length(); j++){
	            policy_table[i][j] = pt_jja.getDouble(j);
	        }
	    }
	    System.out.println("Read " + (pt_ija.length() * pt_ija.getJSONArray(0).length()) + " elements from " + filename + " to Policy Table.");

	     // Read reward_table
	    pt_ija = j_obj.getJSONArray("Reward Table");
	    for (int i = 0; i < pt_ija.length(); i++){
	        JSONArray pt_jja = pt_ija.getJSONArray(i);
	        for (int j = 0; j < pt_jja.length(); j++){
	            reward_table[i][j] = pt_jja.getDouble(j);
	        }
	    }
	    System.out.println("Read " + (pt_ija.length() * pt_ija.getJSONArray(0).length()) + " elements from " + filename + " to Reward Table.");

	    // Read iteration_table
	    JSONArray pit_ija = j_obj.getJSONArray("Iteration Table");
	    for (int i = 0; i < pit_ija.length(); i++){
	        JSONArray pt_jja = pit_ija.getJSONArray(i);
	        for (int j = 0; j < pt_jja.length(); j++){
	            iteration_table[i][j] = pt_jja.getInt(j);
	        }
	    }
	    System.out.println("Read " + (pit_ija.length() * pit_ija.getJSONArray(0).length()) + " elements from " + filename + " to Iteration Table.");
	}

	private void exportPolicy(){
	    System.out.println("Exporting vectors and tables to file.");

        PrintWriter export = null;
        Boolean notBeginning = false;
        try {
            export = new PrintWriter("ref_export.json", "UTF-8");
        } catch (Exception e){
            System.out.println("IO Error exporting.");
            return;
        }
        export.println(indent(0) + "{");

        // Export total_reward
        export.println(indent(1) + "\"Total Reward\": " + total_reward + ",");
        System.out.println("Wrote " + reward_vector.size() + " elements from Total Reward to " + filename + ".");

        // Export policy_table
        notBeginning = false;
        export.println(indent(1) + "\"Policy Table\":");
        export.println(indent(1) + "[");
        Boolean notBeginning2;
        for (double[] pt_i : policy_table){
            if (notBeginning){
                export.println(",");
            }
            export.print(indent(2) + "[");
            notBeginning2 = false;
            for (double pt_j : pt_i){
                if (notBeginning2){
                    export.print(", ");
                }
                export.print(pt_j);
                notBeginning2 = true;
            }
            export.print("]");
            notBeginning = true;
        }
        export.println("\n" + indent(1) + "],");
        System.out.println("Wrote " + policy_table.length * policy_table[0].length + " elements from Policy Table to " + filename + ".");

        // Export reward_table
        notBeginning = false;
        export.println(indent(1) + "\"Reward Table\":");
        export.println(indent(1) + "[");
        for (double[] pt_i : reward_table){
            if (notBeginning){
                export.println(",");
            }
            export.print(indent(2) + "[");
            notBeginning2 = false;
            for (double pt_j : pt_i){
                if (notBeginning2){
                    export.print(", ");
                }
                export.print(pt_j);
                notBeginning2 = true;
            }
            export.print("]");
            notBeginning = true;
        }
        export.println("\n" + indent(1) + "],");
        System.out.println("Wrote " + reward_table.length * reward_table[0].length + " elements from Reward Table to " + filename + ".");

        //Export iteration_table
        notBeginning = false;
        export.println(indent(1) + "\"Iteration Table\":");
        export.println(indent(1) + "[");
        for (int[] pt_i : iteration_table){
            if (notBeginning){
                export.println(",");
            }
            export.print(indent(2) + "[");
            notBeginning2 = false;
            for (int pt_j : pt_i){
                if (notBeginning2){
                    export.print(", ");
                }
                export.print(pt_j);
                notBeginning2 = true;
            }
            export.print("]");
            notBeginning = true;
        }
        export.println("\n" + indent(1) + "]");
        System.out.println("Wrote " + iteration_table.length * iteration_table[0].length + " elements from Iteration Table to " + filename + ".");


        export.println(indent(0) + "}");
        export.close();
	}
	
	public static void main(String[] args) {
		new AgentLoader(new ExMarioAgent()).run();
	}
}
