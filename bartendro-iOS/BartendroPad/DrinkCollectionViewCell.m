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
  
  // If you want rounded corners
  //[self.layer setCornerRadius:10.0f];
  //[self.pourButton.layer setCornerRadius:10.0f];

  
  self.drinkDescription.text = aDrink.desc;
  self.drinkDescription.textColor = [UIColor lightGrayColor];
<<<<<<< HEAD
  self.drinkDescription.font = [UIFont fontWithName:@"DIN Alternate" size:20];

  // Drop shadow: NOTE: does not seem to work at all!
=======
  self.drinkDescription.font = [UIFont fontWithName:@"DIN Alternate Condensed" size:18];
  [self.layer setCornerRadius:10.0f];
  
>>>>>>> 3b753643f470e85a0614fc1663549b0b149d3b42
  [self.layer setShadowColor:[UIColor blackColor].CGColor];
  [self.layer setShadowOpacity:0.8];
  [self.layer setShadowRadius:3.0];
  [self.layer setShadowOffset:CGSizeMake(2.0, 2.0)];
  self.drinkImageView.image = [self getDrinkImageName:aDrink];
  self.drinkName.text = aDrink.name;
  [self setDrink:aDrink];

}


- (IBAction)pourDrink:(id)sender {
  [self.serveDrinkDelegate serveDrinkWithId:[self.drink.drink_id intValue]];
}

-(UIImage*) getDrinkImageName:(Drink*) aDrink {
  NSString * imageName = [[NSString alloc] initWithFormat:@"drink_%@", aDrink.drink_id];
  return [UIImage imageNamed:imageName];
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
