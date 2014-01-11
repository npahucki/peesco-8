//
//  DrinkCollectionViewCell.m
//  BartendroPad
//
//  Created by Pablo Castro on 12/11/13.
//  Copyright (c) 2013 witty. All rights reserved.
//

#import "DrinkCollectionViewCell.h"

@implementation DrinkCollectionViewCell

@synthesize drink;


- (id)initWithFrame:(CGRect)frame
{
    self = [super initWithFrame:frame];
    if (self) {
        // Initialization code
    }
    return self;
}

/*
// Only override drawRect: if you perform custom drawing.
// An empty implementation adversely affects performance during animation.
- (void)drawRect:(CGRect)rect
{
    // Drawing code
}
*/

-(void)populateUIwithDatafrom:(Drink *)aDrink{

    self.backgroundColor = [UIColor whiteColor];
    self.drinkDescription.text = aDrink.desc;
    self.drinkName.text = aDrink.name;
    
    [self setDrink:aDrink];

}


- (IBAction)pourDrink:(id)sender {
    
    NSLog(@"Pouring a drink called: %@", self.drink.name);
    NSLog(@"With the ID: %@", self.drink.drink_id);
    NSLog(@"With ingredients: %@", self.drink.ingredients);

    //[self getDrinkDescription:self.drink.drink_id.intValue];
    
    
    NSArray * ing = self.drink.ingredients;
    
    NSString * args = [[NSString alloc] init];
    
    for (int i=0; i < ing.count; i++) {
        
        NSLog(@"ingrediente %d", i );
        
        if (i == 0) {
            args = @"?";
        }else{
            args = [NSString stringWithFormat:@"%@%@",args, @"&"];
        }
        
        NSDictionary * anIng = [ing objectAtIndex:i];
        
        NSString * boz = [NSString stringWithFormat:@"booze%@=19",[anIng objectForKey:@"id"]];
        args = [NSString stringWithFormat:@"%@%@",args, boz];
        NSLog(@"args: %@", args);
        NSLog(@"/ws/drink/%@%@", [self.drink.drink_id stringValue],args);
        
    }

    

    
    
    
//#     print drink.ingredients
//#
//#     for ing in drink.ingredients:
//#     	print {
//#         'name'           : ing['name'],
//#         'id'             : ing['id'],
//#         'parts'          : ing['parts'],
//#         'newparts'       : 0,
//#         'volume'         : 0,
//#         'taster_volume'  : 0,
//#         'type'           : ing['type']
//#         }
//    
//# for(i = 0; i < ing.length; i++)
//#         {
//#             if (i == 0)
//#                 args = "?";
//#             else
//#                 args += "&";
//#             args += "booze" + ing[i].id + "=";
//#             volume = is_taster ? ing[i].taster_volume.toFixed(0) : ing[i].volume.toFixed(0);
//#             args += volume;
//#         }
// /ws/drink/9?booze4=19&booze3=19&booze2=19&booze1=19&booze6=19&booze7=19&booze5=19&booze8=19
// /ws/drink/9?booze4=19&booze3=19&booze2=19&booze1=19&booze6=19&booze7=19&booze5=19&booze8=19
//
//    NSArray * ingredients = [self.drink.info objectForKey:@"ingredients"];
//    NSString * args = [[NSString alloc] init];
//    
//    for (int i=0; i<ingredients.count; i++) {
//        
//        if (i == 0) {
//            args = @"?";
//        }else{
//            args = [NSString stringWithFormat:@"%@%@",args, @"&"];
//        }
//        
//        NSDictionary * anIng = [ingredients objectAtIndex:i];
//        
//        args = [NSString stringWithFormat:@"booze%@=19",[anIng objectForKey:@"id"]];
//        
//    }
//    
//    NSLog(@"args: %@",args);
    
    
    
    
    
//# $.ajax({
//#                 url: "/ws/drink/" + drink + args,
//#                 success: function(html)
//#                 {
//#                     if (is_taster)
//#                         $.modal.close();
//#                     else
//#                         window.location = "/";
//#                 }
//#         });

    
    
    
}


-(void) getDrinkDescription:(int)drinkID{
    
    NSLog(@"Getting drink with ID: %d", drinkID);
    
    AFHTTPRequestOperationManager * manager = [AFHTTPRequestOperationManager manager];
    
    NSString * wsCall = [[NSString alloc] initWithFormat:@"http://localhost:8080/ws/drink_info/%d", drinkID ];
    
    [manager GET:wsCall
      parameters:nil
     
         success:^(AFHTTPRequestOperation *operation, id responseObject) {
             
             NSLog(@"drink.info :%@", responseObject);
             
             NSArray * tmp = [responseObject objectForKey:@"drink"] ;

             NSDictionary * drk = [tmp objectAtIndex:0];
             
             NSArray * ingredients = [drk objectForKey:@"ingredients"];
             
             NSLog(@"ingredientes: %@", ingredients );
             
             NSString * args = [[NSString alloc] init];
             
             for (int i=0; i<ingredients.count; i++) {
             
                 NSLog(@"ingrediente %d", i );
                 
                 if (i == 0) {
                     args = @"?";
                 }else{
                     args = [NSString stringWithFormat:@"%@%@",args, @"&"];
                 }
                 
                 NSDictionary * anIng = [ingredients objectAtIndex:i];
                 
                 NSString * boz = [NSString stringWithFormat:@"booze%@=19",[anIng objectForKey:@"id"]];
                 args = [NSString stringWithFormat:@"%@%@",args, boz];
                 NSLog(@"args: %@", args);
                 NSLog(@"/ws/drink/%@%@", [self.drink.drink_id stringValue],args);
                 
                 
             }

//             NSLog(@"args: %@",args);

             
             
             
             
         }
     
         failure:^(AFHTTPRequestOperation *operation, NSError *error) {
             NSLog(@"Error: %@", error);
         }
     ];
}





@end
