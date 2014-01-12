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
  
  /*
   
   // border radius
   [v.layer setCornerRadius:30.0f];
   
   // border
   [v.layer setBorderColor:[UIColor lightGrayColor].CGColor];
   [v.layer setBorderWidth:1.5f];
   
   // drop shadow
   [v.layer setShadowColor:[UIColor blackColor].CGColor];
   [v.layer setShadowOpacity:0.8];
   [v.layer setShadowRadius:3.0];
   [v.layer setShadowOffset:CGSizeMake(2.0, 2.0)];
   */
  
  
  
  self.drinkDescription.text = aDrink.desc;
  self.drinkDescription.textColor = [UIColor lightGrayColor];
  self.drinkDescription.font = [UIFont fontWithName:@"DIN Alternate" size:20];
  [self.layer setCornerRadius:10.0f];
  
  [self.layer setShadowColor:[UIColor blackColor].CGColor];
  [self.layer setShadowOpacity:0.8];
  [self.layer setShadowRadius:3.0];
  [self.layer setShadowOffset:CGSizeMake(2.0, 2.0)];
  
  [self.pourButton.layer setCornerRadius:10.0f];
  
  
  self.drinkName.text = aDrink.name;
  
    [self setDrink:aDrink];

}


- (IBAction)pourDrink:(id)sender {

    NSString * get = [NSString stringWithFormat:@"http://%@/ws/drink/%@",BARTENDRO_URL,  self.drink.drink_id];
    
    AFHTTPRequestOperationManager * manager = [AFHTTPRequestOperationManager manager];

    [manager GET:get
      parameters:nil
     
         success:^(AFHTTPRequestOperation *operation, id responseObject) {
             NSLog(@"JSON: %@", responseObject);
         }
     
         failure:^(AFHTTPRequestOperation *operation, NSError *error) {
             NSLog(@"Error: %@", error);
         }
     ];

//    NSLog(@"Pouring a drink called: %@", self.drink.name);
//    NSLog(@"With the ID: %@", self.drink.drink_id);
//    NSLog(@"With ingredients: %@", self.drink.ingredients);
//
//    //[self getDrinkDescription:self.drink.drink_id.intValue];
//    
//    
//    NSArray * ing = self.drink.ingredients;
//    
//    NSString * args = [[NSString alloc] init];
//    
//    for (int i=0; i < ing.count; i++) {
//        
//        NSLog(@"ingrediente %d", i );
//        
//        if (i == 0) {
//            args = @"?";
//        }else{
//            args = [NSString stringWithFormat:@"%@%@",args, @"&"];
//        }
//        
//        NSDictionary * anIng = [ing objectAtIndex:i];
//        
//        NSString * boz = [NSString stringWithFormat:@"booze%@=19",[anIng objectForKey:@"id"]];
//        args = [NSString stringWithFormat:@"%@%@",args, boz];
//        NSLog(@"args: %@", args);
//        NSLog(@"/ws/drink/%@%@", [self.drink.drink_id stringValue],args);
//        
//    }

    

    
    
    
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

-(UIColor*)colorWithHexString:(NSString*)hex
{
  NSString *cString = [[hex stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]] uppercaseString];
  
  // String should be 6 or 8 characters
  if ([cString length] < 6) return [UIColor grayColor];
  
  // strip 0X if it appears
  if ([cString hasPrefix:@"0X"]) cString = [cString substringFromIndex:2];
  
  if ([cString length] != 6) return  [UIColor grayColor];
  
  // Separate into r, g, b substrings
  NSRange range;
  range.location = 0;
  range.length = 2;
  NSString *rString = [cString substringWithRange:range];
  
  range.location = 2;
  NSString *gString = [cString substringWithRange:range];
  
  range.location = 4;
  NSString *bString = [cString substringWithRange:range];
  
  // Scan values
  unsigned int r, g, b;
  [[NSScanner scannerWithString:rString] scanHexInt:&r];
  [[NSScanner scannerWithString:gString] scanHexInt:&g];
  [[NSScanner scannerWithString:bString] scanHexInt:&b];
  
  return [UIColor colorWithRed:((float) r / 255.0f)
                         green:((float) g / 255.0f)
                          blue:((float) b / 255.0f)
                         alpha:1.0f];
}



@end
